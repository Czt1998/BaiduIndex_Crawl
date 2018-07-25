# BaiduIndex_Crawl
Collecting a movie's baiduindex of particular time.
## Main code
* `main.py`<br>
    Call BaiduIndex_Crawl.py and Get_date.py.<br>
* `BaiduIndex_Crawl.py`<br>
    Main code to collect the data from baiduindex.<br>
* `Get_date.py`<br>
    Get the movie's release date.<br>
## Operating environment
Based on python3.5 and selenium, first need to install：<br>
1. `selenium`
2. `pytesseract`
3. `Pillow`
4. `phantomjs`
5. `chromedriver`
## Operation instructions
Star with `main.py` and then it will call the `Get_date` and `BaiduIndex_Crawl.py` to get the data we need.<br>
## Sample
* Let's take 山楂树之恋 as example<br>
* First use its name to get the date from MTime.<br>
![date](https://github.com/Czt1998/BaiduIndex_Crawl/blob/master/pic/date)
* And then use its name and date to get the data from baiduindex.<br>
![](https://github.com/Czt1998/BaiduIndex_Crawl/blob/master/pic/baidu.jpg)
* Store the imformation like this.<br>
movie_name <br>
[date1:data1,date2:data2....]<br>
