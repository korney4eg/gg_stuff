#!/usr/bin/env python3

import logging
import os

logFormat = "%(asctime)s %(levelname)s %(module)s[%(funcName)s:%(lineno)d]: %(message)s"
dateFormat = "%d.%m.%Y %H:%M:%S"
logging.basicConfig(format=logFormat, datefmt=dateFormat, level=logging.DEBUG)

class StyleGenerator():
    def __init__(self, elementsDir=None):
        self.elementsCache = dict()
        self.cacheElements(elementsDir)


    def cacheElements(self, elementsDir=None):
        '''Create elements cache from .css files in given `elementsDir`
        directory.'''
        if elementsDir is None:
            logging.warning("No `elementsDir` specified, abort cache update.")
            return
        if not os.path.isdir(elementsDir):
            logging.error("Elements directory '%s' not found, abort cache update.", elementsDir)
            return

        self.elementsCache = dict()
        for f in os.listdir(elementsDir):
            froot, ext = os.path.splitext(f)
            if ext != ".css":
                continue
            ef = os.path.join(elementsDir, f)
            with open(ef, "rt") as fp:
                cacheKey = self.normalizeCacheKey(froot)
                self.elementsCache[cacheKey] = fp.read()
                logging.info("Put element '%s' from '%s' in cache.", cacheKey, ef)


    def fromString(self, description=None):
        '''Create style from `description`.

        `description` must be multiline text where lines is a .css file
        name from elements directory.

        No need specify full file name in `description`:
        - you can avoid .css extension
        - no matter between space and underscore

        Return generated style as multiline string'''
        if description is None:
            logger.error("No style description provided, return empty style.")
            return ""
        style = str()
        for l in description.splitlines():
            l, _ = os.path.splitext(l)
            cacheKey = self.normalizeCacheKey(l)
            styleBlock = self.elementsCache.get(cacheKey)
            if styleBlock is not None:
                style += (styleBlock + '\n')
        return style


    def fromFile(self, fname):
        '''Create style from description in file `fname`'''
        with open(fname, "rt") as fp:
            description = fp.read()
        return self.fromString(description)


    @classmethod
    def normalizeCacheKey(self, key):
        '''No matter between space and underscore in description,
        right?'''
        return key.replace(' ', '_')


if __name__ == "__main__":
    ELEMENTS_DIR = "elements"
    THEMES_DIR   = "themes"
    CSS_DIR      = "css"

    generator = StyleGenerator(ELEMENTS_DIR)

    if not os.path.isdir(THEMES_DIR):
        logging.error("Themes directory '%s' not found, generator stopped.", elementsDir)
        os.exit(1)

    for t in os.listdir(THEMES_DIR):
        # Read theme description and generate style
        tf = os.path.join(THEMES_DIR, t)
        logging.info("Process theme from '%s'.", tf)
        style = generator.fromFile(tf)

        # Write style to file
        themeName, _ = os.path.splitext(t)
        styleName = os.path.join(CSS_DIR, themeName + ".css")
        if not os.path.exists(CSS_DIR):
            os.mkdir(CSS_DIR, mode=0o755)
        with open(styleName, "wt") as sfp:
            sfp.write(style)
            logging.info("Writed style '%s'", styleName)
