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
|Fill in account|star.sh|main.py|
|:--------------|-------|-------|
|Open the `Get_data.py`, find 'AccountList' in line 11, fill in several account like this ['account','passwd']|Star with `star.sh`, and the it will run the `main.py` to do the task|It will call the `Get_data.py` and `BaiduIndex_Crael.py`.| 
## Sample
* Let's take 山楂树之恋 as example<br>
* First use its name to get the date from MTime.<br>
![date](https://github.com/Czt1998/BaiduIndex_Crawl/blob/master/pic/date)
* And then use its name and date to get the data from baiduindex.<br>
![](https://github.com/Czt1998/BaiduIndex_Crawl/blob/master/pic/baidu.jpg)
* Store the imformation like this.<br><br>
movie_name <br>
[date1:data1,date2:data2....]<br>
[example](https://github.com/Czt1998/BaiduIndex_Crawl/blob/master/pic/4151110.txt)
