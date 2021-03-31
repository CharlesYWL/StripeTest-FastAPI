![image of FastAPI](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)
# How to Run FastAPI
 
### Install and Enter python env
```python
$ virtualenv --no-site-packages --distribute .env 
$ .env/bin/activate 
$ pip install -r requirements.txt
```
### Start FastAPI Server with Command Line
```python
$ cd src
$ uvicorn main:app --reload
```
### Start FastAPI Server with PyCharm
Set Configuration path as: ```\StripeTest\src\main.py```
Add below code to your ```main.py```, These code has already in this repo so you dont need to add that.
```python
import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
```
