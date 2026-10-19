import java.util.Properties

plugins {
    `java-library`
}

group = "org.rednoise"
// Single source of truth for the version is gradle.properties; library.properties is
// verified against it by the checkLibraryVersion task.
version = property("version") as String

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

val processingLib = tasks.register<Zip>("processingLibrary") {
    description = "Assemble the Processing library distribution (rita.zip)"
    group = "distribution"
    archiveBaseName.set("rita")
    archiveVersion.set("")
    archiveClassifier.set("")
    destinationDirectory.set(layout.buildDirectory.dir("distributions"))

    into("rita") {
        from("library.properties")
        from(jarFile) { rename { "rita.jar" } }
        from("examples") { into("examples") }
        from(tasks.named("javadoc")) { into("reference") }
    }
}

val checkLibraryVersion = tasks.register<Task>("checkLibraryVersion") {
    description = "Fail if library.properties disagrees with gradle.properties"
    group = "verification"
    val propsFile = file("library.properties")
    inputs.file(propsFile)
    inputs.property("version", project.version.toString())
    doLast {
        val props = Properties().apply { propsFile.inputStream().use { load(it) } }
        val pretty = props.getProperty("prettyVersion")
        if (pretty != project.version.toString()) {
            throw GradleException(
                "library.properties prettyVersion '$pretty' != project version '${project.version}'. " +
                    "Bump both together.",
            )
        }
    }
}

tasks.named("check") { dependsOn(checkLibraryVersion) }
tasks.named("build") { dependsOn(processingLib) }
