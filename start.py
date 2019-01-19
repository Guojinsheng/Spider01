import scrapy.cmdline


def main():
    # scrapy.cmdline.execute("scrapy crawl myxima".split())
    scrapy.cmdline.execute("scrapy crawl myxima --nolog".split())


if __name__ == '__main__':
    main()
