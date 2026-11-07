package com.example.bedrockui;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.screen.v1.ScreenEvents;
import net.fabricmc.fabric.api.client.screen.v1.Screens;
import net.minecraft.client.gui.components.AbstractWidget;
import net.minecraft.client.gui.screens.Screen;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

/**
 * Bedrock UI: the look (bevelled buttons, sliders, tabs, stone panels) comes entirely from
 * overriding vanilla GUI sprites/textures in assets/minecraft. This class only handles the
 * "big button" layout on the main menu screens, with no mixins.
 */
public class BedrockUiClient implements ClientModInitializer {
    /** Matched by simple class name so a package move between versions doesn't break compilation. */
    private static final Set<String> BIG_BUTTON_SCREENS = Set.of("TitleScreen", "PauseScreen", "OptionsScreen");
    private static final int VANILLA_HEIGHT = 20;

    @Override
    public void onInitializeClient() {
        BedrockUiConfig.load();
        ScreenEvents.AFTER_INIT.register((client, screen, width, height) -> {
            if (BedrockUiConfig.bigButtons && BIG_BUTTON_SCREENS.contains(screen.getClass().getSimpleName())) {
                enlarge(screen, height);
            }
        });
    }

    private static void enlarge(Screen screen, int screenHeight) {
        int newH = BedrockUiConfig.bigButtonHeight;
        List<AbstractWidget> targets = new ArrayList<>();
        for (AbstractWidget w : Screens.getButtons(screen)) {
            boolean wide = w.getWidth() >= BedrockUiConfig.bigButtonMinWidth;
            boolean notFooter = w.getY() < screenHeight - 36; // leave "Done" style footer buttons alone
            if (w.visible && w.getHeight() == VANILLA_HEIGHT && wide && notFooter) targets.add(w);
        }
        if (targets.size() < 2) return;

        int minY = Integer.MAX_VALUE, maxY = Integer.MIN_VALUE;
        for (AbstractWidget w : targets) { minY = Math.min(minY, w.getY()); maxY = Math.max(maxY, w.getY()); }

        double scale = (double) newH / VANILLA_HEIGHT;
        double oldCenter = (minY + maxY + VANILLA_HEIGHT) / 2.0;
        // shrink the scale if the stack would run off the screen
        while (scale > 1.0) {
            double span = (maxY - minY) * scale + newH;
            if (oldCenter - span / 2.0 >= 6 && oldCenter + span / 2.0 <= screenHeight - 6) break;
            scale -= 0.05;
        }
        int h = (int) Math.round(VANILLA_HEIGHT * Math.max(1.0, scale));
        double newTop = oldCenter - ((maxY - minY) * scale + h) / 2.0;

        for (AbstractWidget w : targets) {
            w.setY((int) Math.round(newTop + (w.getY() - minY) * scale));
            w.setHeight(h);
        }
    }
}
