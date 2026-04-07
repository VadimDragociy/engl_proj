This is a MVP face recognition system created for project fair held by Foreighn Languages Department of MIPT, Russia

## Technologies
1) Face embeddings - insightface.Buffalo_l
2) Database - sqlite3
3) Ui - FastApi + html

## Algorithm

Face embeddings are created directly from the video feed (with a framerate around 10 fps on 3050 mobile gpu (4 gb VRam))

Afterwards embeddings are compared to each entry in the database

Right now Webpage serves both for uploading new users into database and for face recognition


## To start:
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```