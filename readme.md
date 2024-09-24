# Bing Gallery

Command-line tool for change a desktop picture based on daily [Bing](https://www.bing.com) images

[![Build Status](https://travis-ci.org/vitalibo/bing-gallery.svg?branch=master)](https://travis-ci.org/vitalibo/bing-gallery)

### Installing
#### macOS

For macOS family you can use [Homebrew](https://brew.sh) package for that.

```bash
wget https://raw.githubusercontent.com/vitalibo/bing-gallery/master/integration/brew/bing-gallery.rb
brew install bing-gallery.rb
```

### Usage

```text
usage: bing_gallery [--offset {1..7}] [--market {en-US,zh-CN,ja-JP,en-AU,en-UK,de-DE,en-NZ,en-CA}] 
                    [--output OUTPUT] [--version] [-h]

Command-line tool for change a desktop picture based on daily Bing images

optional arguments:
  --offset {0,1,2,3,4,5,6,7}
                        Specify index of photo to use.
  --market {en-US,zh-CN,ja-JP,en-AU,en-UK,de-DE,en-NZ,en-CA}
                        Specify market that you want to use.
  --output OUTPUT       Output folder for storing images.
  --version             Display the version of this tool.
  -h, --help            Show this help message.

Copyright (c) 2015-2020, Vitaliy Boyarsky
```
