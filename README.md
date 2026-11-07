# Bedrock UI (Fabric, client-side)

Look: original Bedrock-style pixel art overriding vanilla GUI sprites (`assets/minecraft/textures/gui/...`):
buttons (normal/hover/disabled), sliders, text fields, tabs, stone menu/list backgrounds, header/footer separators.
Layout: taller, re-spaced buttons on Title / Pause / Options screens (no mixins).
Config: `config/bedrock_ui.properties` (`big_buttons`, `big_button_height`, `big_button_min_width`).

Restyle: edit colours in `tools/gen_textures.py` and run `python3 tools/gen_textures.py`, or drop in your own PNGs.
Setup: put the right versions for MC 26.3 from https://fabricmc.net/develop/ into `gradle.properties`, then `./gradlew build`
If `gradlew` is missing (it needs a binary jar I couldn't generate), run `gradle wrapper --gradle-version 9.2.0` once and commit
`gradlew`, `gradlew.bat` and `gradle/wrapper/`. Output jar: `build/libs/`.

CI: `.github/workflows/build.yml` builds on every push/PR and uploads the jar as an artifact.
Push a tag like `v1.0.0` to also create a GitHub Release with the jar. Keep the Java version (25) and Gradle version
in the workflow in sync with what Loom for 26.3 needs.
