# Zhihu crawler

Regularly crawl zhihu hot list (every 10 minutes by default), and record the basic information of the hot list questions, such as question summary, description, heat, number of visitors, number of answers, and so on. Then store these data in the database for preservation.

## Usage

1. Put your personal information into `zhihu.json` in the same directory as `zhihu.py`. The format is like:
   ```json
   {
        "headers": {
            "User-Agent":"",
            "Cookie":""
        },
        "config": {
            "interval_between_board": 600,
            "interval_between_question": 2
        },
        "mysql": {
            "host": "",
            "user": "",
            "password": "",
            "database": "",
            "charset": "",
            "port": -1
        }
    }
    ```
2. Just run the code: `python3 zhihu.py`. If the program works well, you will see some log information similar to the following:
    ```
    2022-07-17 10:17:16.693 [INFO] Settings loaded
    2022-07-17 10:17:30.684 [INFO] Begin crawling ...
    2022-07-17 10:17:43.066 [INFO] Get 50 items: 如何看待四川若尔盖缉枪治爆，群众上缴枪支,如何看待运动员苏炳添称「 对不起大家但我,第 63 届国际数学奥赛中国队满分摘金，,工商银行表示 8 月 15 日起暂停账户,为什么会有「去外地旅游，尽量别联系以前的,英国宣布进入国家紧急状态并首次发布极端高,建筑工回家路上倒下因热射病去世，家属称未,2021 年出生人口下降 140 万，专,成年人能打过扬子鳄吗?,手动挡汽车为什么没有了？,美国被曝又宣布 1.08 亿美元对台军售,为什么祁同伟觉得高育良政治手段高明却从不,如何看待李想回应理想 L9 铸铁下摆「装,放弃吉大，兰大，海大，农大等 985 选,小布丁大布丁等雪糕蛋白质等项目抽检不合格,2022 KPL 夏季赛 GK 3:0 ,中国是世界上最重视女足的国家，也是女足起,灭绝师太将掌门之位传给周芷若而不是丁敏君,有什么本地人不怎么吃，外地人却以为是「当,2022 男篮亚洲杯小组赛中国男篮 95,张亮麻辣烫回应「闽南香肉」标注含狗肉，称,提到避暑，你脑海中出现的第一个地方是哪里,如何解读罗兰贝格发布的《中国跨境航空货运,因为家庭条件，读与不读我该如何选择？,如果给你一个回到过去的机会，你会怎么做？,大一新生带两个行李箱会很奇怪吗？,通胀爆表，加息预期炸了，但为何美股没有大,如何看待小米 12S ultra 好评率,完全跟不上全英文授课的节奏怎么办？,我是一名程序员，深夜加班吃了外派公司的零,农村的葬礼有必要搞的那么复杂吗？,你有过身高被碾压的经历吗?,南昌室外核酸采样员不再穿防护服，改穿一次,两个实打实干活的同事离职了，老板连谈都没,运 -12 拥有 14 个国家的适航证，,如何看待国内首个抗新冠口服药阿兹夫定片提,准大一新生，到底是住寝室好，还是不住寝室,为什么《英雄联盟》现在新出的英雄都很少叫,如何评价网传北京大学 2022 年在内蒙,2022 世界田径锦标赛男子 100 米,如何看待北京时间 7 月 17 日 UF,如何看待杨超越说贷款买房好焦虑登上热搜？,第一个让你感到真正恐惧的电子游戏是什么？,当你落魄的从原单位出来，通过努力你成为了,7 月 16 日上海新增本土确诊 2 例,什么是买断制游戏？,欧盟禁止从俄进口黄金，西方预计俄每年损失,为什么收入越多，却感觉越来越穷？,新手如何系统性地学习摄影？,你知道哪些行业内公开的秘密？
    2022-07-17 10:17:43.067 [INFO] Sleep 2 second(s)
    2022-07-17 10:17:45.583 [INFO] Get question detail for 如何看待四川若尔盖缉枪治爆，群众上缴枪支 198 支，手榴弹 10 枚？私藏枪支可能会受到什么处罚？: raw detail length 2780
    2022-07-17 10:17:54.653 [INFO] Sleep 2 second(s)
    2022-07-17 10:17:57.372 [INFO] Get question detail for 如何看待运动员苏炳添称「 对不起大家但我会继续努力 」？运动员比赛表现不理想需要道歉吗？: raw detail length 1158
    2022-07-17 10:18:06.427 [INFO] Sleep 2 second(s)
    2022-07-17 10:18:08.963 [INFO] Get question detail for 第 63 届国际数学奥赛中国队满分摘金，系 28 年来首次，如何评价这支队伍的实力？: raw detail length 498
    2022-07-17 10:18:18.202 [INFO] Sleep 2 second(s)
    ...
    ```

Sample crawled information is recorded in `zhihu.sql.gz`.