import sqlalchemy
from pprint import pprint

from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime

engine = sqlalchemy.create_engine('postgresql://julija:@localhost:5432/bazadannih')

engine

connection = engine.connect()

'''1. Количество исполнителей в каждом жанре'''
zap1 = connection.execute(
"""
SELECT genres.genre_name, COUNT(Performes_Genres.performers_id)
    FROM genres
    JOIN Performes_Genres ON genres.id = Performes_Genres.genres_id
    GROUP BY genres.genre_name;
""").fetchall()

'''2. Количество треков, вошедших в альбомы 2019-2020 годов'''
zap2 = connection.execute(
"""
SELECT albums.title, albums.year_of_issue, COUNT(treks.id)
    FROM albums
    JOIN treks ON albums.id = treks.albums_id
    WHERE albums.year_of_issue BETWEEN 2019 and 2020
    GROUP BY albums.title, albums.year_of_issue;
""").fetchall()

'''3. Средняя продолжительность треков по каждому альбому'''
zap3 = connection.execute(
"""
SELECT albums.title, ROUND(AVG(treks.duration), 0)
    FROM albums
    JOIN treks ON albums.id = treks.albums_id
    GROUP BY albums.title;
""").fetchall()

'''4. Все исполнители, которые не выпустили альбомы в 2020 году'''
zap4 = connection.execute(
"""
SELECT performers.performers_name
    FROM performers
    JOIN performers_albums ON performers.id = performers_albums.performers_id
    JOIN albums ON performers_albums.albums_id = albums.id
    WHERE albums.year_of_issue != 2020
    GROUP BY performers.performers_name;
""").fetchall()

'''5. Названия сборников, в которых присутствует конкретный исполнитель (выберите сами)'''
zap5 = connection.execute(
"""
SELECT collection.name
    FROM collection
    JOIN collection_of_tracks_and_albums ON collection.id = collection_of_tracks_and_albums.collection_id
    JOIN treks ON collection_of_tracks_and_albums.trek_id = treks.id
    JOIN albums ON treks.albums_id = albums.id
    JOIN performers_albums ON albums.id = performers_albums.albums_id
    JOIN performers ON performers_albums.performers_id = performers.id
    WHERE performers.performers_name LIKE ('Lusi')
    GROUP BY collection.name;
""").fetchall()

'''6. Название альбомов, в которых присутствуют исполнители более 1 жанра'''
zap6 = connection.execute(
"""
SELECT albums.title
    FROM albums
    JOIN performers_albums ON albums.id = performers_albums.albums_id
    JOIN performers ON performers_albums.performers_id = performers.id
    JOIN Performes_Genres ON performers.id = Performes_Genres.performers_id
    GROUP BY albums.title
    HAVING COUNT(Performes_Genres.genres_id) > 1;
""").fetchall()

'''7. Наименование треков, которые не входят в сборники'''
zap7 = connection.execute(
"""
SELECT treks.trek_name
    FROM treks
    LEFT JOIN collection_of_tracks_and_albums ON treks.id = collection_of_tracks_and_albums.trek_id
    WHERE collection_of_tracks_and_albums.trek_id IS NULL;
""").fetchall()

'''8. исполнителя(-ей), написавшего самый короткий по продолжительности трек
      (теоретически таких треков может быть несколько)'''
zap8 = connection.execute(
"""
SELECT performers.performers_name
    FROM performers
    JOIN performers_albums ON performers.id = performers_albums.performers_id
    JOIN albums ON performers_albums.albums_id = albums.id
    JOIN treks ON albums.id = treks.albums_id
    WHERE treks.duration = (
        SELECT MIN(duration) FROM treks);
""").fetchall()

'''9. Название альбомов, содержащих наименьшее количество треков'''
zap9 = connection.execute(
"""
SELECT albums.title, COUNT(treks.id)
    FROM albums
    JOIN treks ON albums.id = treks.albums_id
    GROUP BY albums.title
    HAVING COUNT(treks.id) = (
        SELECT COUNT(treks.id)
        FROM albums
        JOIN treks ON albums.id = treks.albums_id
        GROUP BY albums.title
        ORDER BY COUNT(treks.id)
        LIMIT 1)
""").fetchall()

pprint(zap9)

