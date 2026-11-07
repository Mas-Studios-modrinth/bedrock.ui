package com.example.bedrockui;

import net.fabricmc.loader.api.FabricLoader;

import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

/** Tiny properties config: config/bedrock_ui.properties */
public final class BedrockUiConfig {
    public static boolean bigButtons = true;
    public static int bigButtonHeight = 28;
    public static int bigButtonMinWidth = 98;

    public static void load() {
        Path file = FabricLoader.getInstance().getConfigDir().resolve("bedrock_ui.properties");
        Properties p = new Properties();
        if (Files.exists(file)) {
            try (Reader r = Files.newBufferedReader(file)) { p.load(r); } catch (IOException ignored) { }
        }
        bigButtons = Boolean.parseBoolean(p.getProperty("big_buttons", "true"));
        bigButtonHeight = parse(p.getProperty("big_button_height"), 28, 20, 40);
        bigButtonMinWidth = parse(p.getProperty("big_button_min_width"), 98, 20, 400);
        p.setProperty("big_buttons", Boolean.toString(bigButtons));
        p.setProperty("big_button_height", Integer.toString(bigButtonHeight));
        p.setProperty("big_button_min_width", Integer.toString(bigButtonMinWidth));
        try (Writer w = Files.newBufferedWriter(file)) { p.store(w, "Bedrock UI"); } catch (IOException ignored) { }
    }

    private static int parse(String s, int def, int min, int max) {
        try { return Math.max(min, Math.min(max, Integer.parseInt(s.trim()))); }
        catch (Exception e) { return def; }
    }
}
