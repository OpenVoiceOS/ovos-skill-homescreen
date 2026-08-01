# OpenVoiceOS Home Screen

This skill provides the home screen for OpenVoiceOS. It is the first screen you see after onboarding, and it shows widgets for the current date, time, and weather.

![](https://github.com/OpenVoiceOS/ovos_assets/raw/master/Images/homescreen.png)

## Features

### Night mode

Night mode switches the home screen into a dark standby clock. This reduces the light the device emits, which helps in a dark room or at night. To enable night mode, tap the left edge pill button on the home screen.

![](https://github.com/OpenVoiceOS/ovos_assets/raw/master/Images/homescreen-nightmode.gif)

### Quick actions dashboard

The quick actions dashboard is a card-based interface for your most used actions, such as adding an alarm, starting a timer, or adding a note. Tap the plus button in the top right corner of the dashboard to add a custom action. Open the dashboard by tapping the right edge pill button on the home screen.

![](https://github.com/OpenVoiceOS/ovos_assets/raw/master/Images/homescreen-dashboard.gif)

### Application launcher

OpenVoiceOS supports dedicated voice applications. A voice application can be a skill or a PHAL plugin with its own user interface. The application launcher lists all available voice applications. Open it by tapping the center pill button at the bottom of the home screen.

![](https://github.com/OpenVoiceOS/ovos_assets/raw/master/Images/homescreen-app-drawer.png)

### Wallpapers

The home screen supports custom wallpapers and includes a set of wallpapers to choose from. To change the wallpaper, swipe right to left on the home screen.

![](https://github.com/OpenVoiceOS/ovos_assets/raw/master/Images/homescreen_wallpapers.gif)

## Widgets

![](https://github.com/OpenVoiceOS/ovos_assets/raw/master/Images/homescreen-widgets.png)

### Notifications widget

The notifications widget shows a bell icon in the top left corner of the home screen when you have notifications. Tap the bell icon to open the notifications overview.

### Timer widget

The timer widget appears in the top left corner, after the notifications bell icon, when a timer is running. Tap the timer widget to open the timers overview.

### Alarm widget

The alarm widget appears in the top left corner, after the timer widget, when an alarm is set. Tap the alarm widget to open the alarms overview.

### Media player widget

The media player widget appears at the bottom of the home screen and replaces the examples widget when a media player is active. It shows the media that is currently playing and lets you pause, resume, or skip it. Tap the quick display media player button on the right side of the widget to open the media player.

![](https://github.com/OpenVoiceOS/ovos_assets/raw/master/Images/homescreen-mediawidget.gif)

## Configuration

### Settings

Configure the home screen with the standard [skill settings mechanism](https://openvoiceos.github.io/community-docs/115-ht_config_homescreen/).

Sample `settings.json` file with all options:

```
{
  "weather_skill": "skill-weather.openvoiceos",
  "datetime_skill": "skill-date-time.mycroftai",
  "examples_skill": "ovos-skills-info.openvoiceos",
  "wallpaper": "default.jpg",
  "persistent_menu_hint": true,
  "examples_enabled": false,
  "randomize_examples": true,
  "examples_prefix": false
}
```

* `weather_skill`: the skill that shows the weather. Defaults to `skill-ovos-weather.openvoiceos`.
* `datetime_skill`: the skill that shows the date and time. Defaults to `skill-ovos-date-time.openvoiceos`.
* `examples_skill`: the skill that provides the displayed examples. Defaults to the `ovos_skills_manager.utils.get_skills_example()` function.
* `wallpaper`: a custom wallpaper. Use a complete URL, without a tilde (`~`).
* `persistent_menu_hint`: when true, shows a hint of the pull-down menu at the top of the page.
* `examples_enabled`: when false, hides the examples at the bottom of the screen.
* `randomize_examples`: when false, shows examples in the order they load, without shuffling them.
* `examples_prefix`: when false, does not show the "Ask Me" prefix with the examples.

`settings.json` is located at:

* OVOS: `~/.config/mycroft/skills/skill-ovos-homescreen.openvoiceos/settings.json`
* Neon: `~/.config/neon/skills/skill-ovos-homescreen.openvoiceos/settings.json`

For other OVOS-based installations, try the OVOS location first. It is the default.

## Related projects

* [OpenVoiceOS/ovos-gui](https://github.com/OpenVoiceOS/ovos-gui) — the GUI service this skill's interface runs on.
* [OpenVoiceOS/ovos-shell](https://github.com/OpenVoiceOS/ovos-shell) — the shell used on OVOS devices.

## License

Apache-2.0
