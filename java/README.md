# RiTa for Java

Tools for generative natural language — the Java implementation of RiTa.

**Requirements:** JDK 11+ (the Gradle wrapper is checked in, so no Gradle install is needed)

## Build

```sh
./gradlew build                # compile, test, and build rita.jar + rita.zip + rita.txt
./gradlew test                 # run tests only
./gradlew javadoc              # API reference docs
./gradlew processingLibrary    # build/distributions/rita.zip (Processing library)
```

For Processing Manager submission, the release must host `rita.zip` and `rita.txt` (a copy
of `library.properties`) at the same stable URL, differing only by extension — see the
[Library Guidelines](https://github.com/processing/processing4/wiki/Library-Guidelines#release-artifacts).
Both are produced into `build/distributions/` by `./gradlew build`.

The artifact is `org.rednoise:rita`, versioned in [`gradle.properties`](gradle.properties).
The version fields in `library.properties` are expanded from it at build time
(`version` = Processing Manager revision, e.g. `403`; `prettyVersion` = e.g. `4.0.3`), so
bumping `gradle.properties` is the only edit needed.

## Layout

```
java/
├── build.gradle.kts          # build, shared-data staging, Processing packaging
├── library.properties        # Processing library metadata
├── examples                  # example sketches, bundled into the library
└── src/
    ├── main/java/rita/       # library sources (package `rita`)
    ├── main/resources/rita/  # version.properties (dict data is staged, not committed)
    └── test/java/rita/       # tests
```

## Shared data

The canonical dictionary lives in [`../shared/rita_dict.json`](../shared/rita_dict.json) and
is staged onto the classpath at `rita/rita_dict.json` by the `syncSharedData` task — nothing
is generated into this folder, so it can't drift from the source of truth. Load it with:

```java
RiTa.class.getResourceAsStream("/rita/rita_dict.json")
```

## Using as a Processing library

Unzip `build/distributions/rita.zip` into your Processing libraries folder:

```sh
unzip build/distributions/rita.zip -d ~/Documents/Processing/libraries/
```

Then in a sketch:

```java
import rita.*;

void setup() {
  println(RiTa.tokenize("How now, brown cow?"));
  println(RiTa.evaluate("i [ have | own ] a [ blue | green ] [ bird | fish ]"));
}
```