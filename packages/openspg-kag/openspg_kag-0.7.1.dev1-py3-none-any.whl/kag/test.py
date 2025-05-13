from kag.builder.component.scanner.yuque_scanner import YuqueScanner


if __name__ == "__main__":
    rc = YuqueScanner("1yPz1LbE20FmXvemCDVwjlSHpAp18qtEu7wcjCfv")
    #data = rc.load_data("https://yuque-api.antfin-inc.com/api/v2/repos/ob46m2/it70c2/docs/")
    #print(data)
    from kag.builder.component.reader.markdown_reader import  YuequeReader
    reader=YuequeReader(cut_depth=0)
    out ={}
    for url in rc.generate("https://yuque-api.antfin-inc.com/api/v2/repos/ob46m2/it70c2/docs/"):
        res=reader.invoke(url)
        out[url]=res
    print(out)