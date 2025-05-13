# Mapilliary nearby
**@readwithai** - [X](https://x.com/readwithai) - [blog](https://readwithai.substack.com/) - [machine-aided reading](https://www.reddit.com/r/machineAidedReading/) - [📖](https://readwithai.substack.com/p/what-is-reading-broadly-defined
)[⚡️](https://readwithai.substack.com/s/technical-miscellany)[🖋️](https://readwithai.substack.com/p/note-taking-with-obsidian-much-of)

Get photos near a location using the [Mapillary](https://www.mapillary.com/) open source streetview image database.

## Motivation
I like to set up my computer so that it reinforces habits. I am planning to visit another country for a while and learn some languages. A nice way to reinforce this and make this real is to regularly set my background to images in this area.

This tool lets you fetch images in an area. Which you can then set as your background using an appropriate tool.

# Installation
This program uses the mapillary API. To do this, you must create an app for your use of this url.

1. Go to `https://www.mapillary.com/dashboard/developers`
1. Click `Register application`
1. Fill in any details you like
1. Unforunately, you need to add a redirect URL and a company website. But these can be any value
1. The app must have read permission.
1. Once the App is registered copy the client token.

You can then install mapillary-nearby with `pipx`.
```
pipx install mapillary-nearby
```

## Usage
Find the [latitude and longitude](https://en.wikipedia.org/wiki/Longitude) of the location where you want to take images from. I like to use Wikipedia for this - most pages for cities have this information. Get this in decimal rather than minute/second based format.

You can then run, for example
```
mapillary-nearby --lat 56.156389 --long 10.209722  --radius 5000m  test.jpeg
```
To fetch a random photo within 5km on this location and write it to test.jpeg

## Caveats
Upon using this I immediately wanted to know where the pictures were taken. I may add some sort of feature to display locations on a map.

This tool only fetched an image you need to do the "last mile" of setting he background. On linux systems you can use [feh](https://wiki.archlinux.org/title/Feh).

This software probably doesn't work with windows - but will be easy to adapt for those familiar with Python. Pull requests to add support for windows will be quickly merged.

## Support
This makes use of the very using Mapillary service and dataset which is generating a permanently useable set of data for the entire world.

If you find this tool useful you might consider installing mapillary on your phone and collecting some data when you walk around - which I do quite regularly.

## About me
I am @readwithai. I make tools for reading, research and agency sometimes using Obsidian.

You can follow me on [X](https://x.com/readwithai), or bluesky.

You might like to [read about computer-aided habit formation](https://readwithai.substack.com/p/using-computers-to-support-habits).

[![@readwithai logo](./logo.png)](https://readwithai.substack.com/)
