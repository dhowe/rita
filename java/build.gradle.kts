import java.util.Properties

plugins {
    `java-library`
}

group = "org.rednoise"
// Single source of truth for the version is gradle.properties; library.properties is a
// template whose version fields are expanded at build time (see processLibraryProperties).
version = property("version") as String

// Processing Manager's numeric revision for a semantic version: 4.0.3 -> 403
// (major*100 + minor*10 + patch). Keep patch < 10 so the mapping stays unambiguous.
val versionNum = project.version.toString()
    .split('.')
    .map { it.toInt() }
    .let { (major, minor, patch) -> major * 100 + minor * 10 + patch }

repositories {
    mavenCentral()
}

java {
    // No toolchain block: compile against the running JDK with --release so a single
    // JDK install is enough. Processing 4 runs on Java 17, but 11 keeps the artifact
    // usable from plain-JDK builds and older Processing installs.
    withJavadocJar()
}

tasks.withType<JavaCompile>().configureEach {
    options.release.set(11)
    options.encoding = "UTF-8"
}

tasks.withType<Javadoc>().configureEach {
    options {
        encoding = "UTF-8"
        (this as CoreJavadocOptions).addStringOption("Xdoclint:none", "-quiet")
        addBooleanOption("html5", true)
        addBooleanOption("quiet", true)
    }
    // TODO(port): remove once rita.* classes exist. Javadoc exits non-zero with
    // "No public or protected classes found to document" while the port is empty.
    isFailOnError = false
}

// ---------------------------------------------------------------------------
// Shared data
//
// shared/rita_dict.json is the canonical dictionary for every implementation.
// It is staged into the build rather than copied into java/ — no generated
// file in git, so it can never drift from the source of truth.
// ---------------------------------------------------------------------------

val sharedDir = rootDir.toPath().parent.resolve("shared").toFile()
val sharedDict = sharedDir.resolve("rita_dict.json")

val sharedLts = sharedDir.resolve("rita_lts.json")

val syncSharedData = tasks.register<Sync>("syncSharedData") {
    description = "Stage shared/rita_dict.json + rita_lts.json into the build resources (jar path: rita/)"
    group = "build"
    from(sharedDict) { into("rita") }
    from(sharedLts) { into("rita") }
    into(layout.buildDirectory.dir("generated/resources"))
    doFirst {
        if (!sharedDict.exists()) {
            throw GradleException("Missing canonical dictionary: $sharedDict")
        }
        if (!sharedLts.exists()) {
            throw GradleException("Missing canonical LTS rules: $sharedLts")
        }
    }
}

// Test fixtures (shared/*.json) are staged onto the test classpath under fixtures/ so
// data-driven suites can load them as a resource from any working directory.
val syncFixtures = tasks.register<Sync>("syncFixtures") {
    description = "Stage shared/*.json onto the test classpath (fixtures/<name>.json)"
    group = "build"
    from(sharedDir) {
        include("*.json")
        into("fixtures")
    }
    // harvard-data.json lives in js/test/ (a JS-authored fixture), not shared/.
    from(rootDir.toPath().parent.resolve("js").resolve("test").toFile()) {
        include("harvard-data.json")
        into("fixtures")
    }
    into(layout.buildDirectory.dir("generated/test-resources"))
}

sourceSets {
    main {
        resources {
            srcDir(layout.buildDirectory.dir("generated/resources"))
        }
    }
    test {
        resources {
            srcDir(layout.buildDirectory.dir("generated/test-resources"))
        }
    }
}

tasks.processResources {
    dependsOn(syncSharedData)
    filesMatching("**/version.properties") {
        expand("version" to project.version)
    }
}

tasks.processTestResources {
    dependsOn(syncFixtures)
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.11.4"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
    // Test-only JSON reader for the shared fixtures (shared/*.json). The library itself
    // stays dependency-free; Processing libraries must not drag in shaded jars.
    testImplementation("com.google.code.gson:gson:2.11.0")
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
    }
}

// ---------------------------------------------------------------------------
// Processing library packaging
//
// Produces build/distributions/rita.zip unpacking to:
//   rita/library.properties
//   rita/rita.jar
//   rita/reference/          (javadoc)
//   rita/examples/...
// ---------------------------------------------------------------------------

val jarFile = tasks.named<Jar>("jar") {
    manifest {
        attributes(
            "Implementation-Title" to "RiTa",
            "Implementation-Version" to project.version,
            "Implementation-Vendor" to "rednoise.org",
        )
    }
}

// library.properties is a template: ${version} / ${versionNum} are filled in from
// gradle.properties, so the version is bumped in exactly one place.
val processLibraryProperties = tasks.register<Copy>("processLibraryProperties") {
    description = "Expand version fields in library.properties from gradle.properties"
    group = "build"
    inputs.property("version", project.version.toString())
    inputs.property("versionNum", versionNum.toString())
    from(file("library.properties")) {
        expand("version" to project.version.toString(), "versionNum" to versionNum.toString())
    }
    into(layout.buildDirectory.dir("generated/library"))
}

val processingLib = tasks.register<Zip>("processingLibrary") {
    description = "Assemble the Processing library distribution (rita.zip)"
    group = "distribution"
    archiveBaseName.set("rita")
    archiveVersion.set("")
    archiveClassifier.set("")
    destinationDirectory.set(layout.buildDirectory.dir("distributions"))

    into("rita") {
        from(processLibraryProperties)
        from("examples") { into("examples") }
        from(tasks.named("javadoc")) { into("reference") }
        // Processing's Library.discover() only recognises a folder whose jar lives at
        // <name>/library/<name>.jar — a jar at the library root is silently skipped.
        from(jarFile) {
            into("library")
            rename { "rita.jar" }
        }
    }
}

// Processing's Library Guidelines require the release artifacts to share a base name and
// sit in the same directory: rita.zip plus rita.txt (a direct copy of the expanded
// library.properties). See https://github.com/processing/processing4/wiki/Library-Guidelines
val processingLibraryPropertiesTxt = tasks.register<Copy>("processingLibraryPropertiesTxt") {
    description = "Emit rita.txt (copy of library.properties) alongside rita.zip"
    group = "distribution"
    dependsOn(processLibraryProperties)
    from(processLibraryProperties) {
        rename { "rita.txt" }
    }
    into(layout.buildDirectory.dir("distributions"))
}

val checkLibraryVersion = tasks.register<Task>("checkLibraryVersion") {
    description = "Fail if the expanded library.properties disagrees with gradle.properties"
    group = "verification"
    dependsOn(processLibraryProperties)
    val expanded = layout.buildDirectory.file("generated/library/library.properties")
    inputs.file(expanded)
    inputs.property("version", project.version.toString())
    // Capture at configuration time: touching Task.project inside doLast is deprecated
    // (Task.project at execution time) and fails under the configuration cache in Gradle 10.
    val expectedPretty = project.version.toString()
    val expectedNumeric = versionNum.toString()
    doLast {
        val props = Properties().apply { expanded.get().asFile.inputStream().use { load(it) } }
        val pretty = props.getProperty("prettyVersion")
        val numeric = props.getProperty("version")
        if (pretty != expectedPretty || numeric != expectedNumeric) {
            throw GradleException(
                "library.properties (prettyVersion=$pretty, version=$numeric) does not match " +
                    "project version '$expectedPretty' (numeric $expectedNumeric).",
            )
        }
    }
}

tasks.named("check") { dependsOn(checkLibraryVersion) }
tasks.named("build") { dependsOn(processingLib, processingLibraryPropertiesTxt) }
