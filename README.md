# MangaReader API

## Introduction
This is documentation for a scraper api for [mangareader](https://mangareader.to/)

## Getting Started
To get started with the Manga API, follow the steps below:
1. Clone the repository: `git clone https://github.com/thullyDev/MangaNato.api.git`
2. Install dependencies: `pip3 install -r requirements.txt` or `pip install -r requirements.txt`
3. Run the API: `uvicorn app.main:app`

## Endpoints

### Get Featured Mangas

- **URL:** `/manga/features`
- **Method:** GET
- **Description:** Get featured mangas.
- **Response:** Returns featured mangas data.

### Filter Mangas

- **URL:** `/manga/filter`
- **Method:** GET
- **Description:** Filter mangas based on various parameters.
- **Parameters:**
  - `language` (optional): Language of the manga.
  - `genres` (optional): Genre(s) of the manga.
  - `sort` (optional): Sorting criteria.
  - `status` (optional): Status of the manga.
  - `read_type` (optional): Type of reading.
  - `rating_type` (optional): Type of rating.
  - `keyword` (optional): Keyword to search for.
  - `page` (optional): Page number (default: 1).
- **Response:** Returns filtered mangas data.

### Get Mangas by Genre

- **URL:** `/manga/genre/{genre_ID}`
- **Method:** GET
- **Description:** Get mangas by genre.
- **Parameters:**
  - `{genre_ID}`: Genre ID.
  - `page` (optional): Page number (default: 1).
- **Response:** Returns mangas data based on the specified genre.

### Get Mangas by Type

- **URL:** `/manga/type/{type_ID}`
- **Method:** GET
- **Description:** Get mangas by type.
- **Parameters:**
  - `{type_ID}`: Type ID.
  - `page` (optional): Page number (default: 1).
- **Response:** Returns mangas data based on the specified type.

### Read Chapter

- **URL:** `/manga/read/{chapter_ID}`
- **Method:** GET
- **Description:** Read a chapter of a manga.
- **Parameters:**
  - `{chapter_ID}`: Chapter ID.
- **Response:** Returns chapter data.

### Get Manga Details

- **URL:** `/manga/{manga_ID}`
- **Method:** GET
- **Description:** Get details of a manga.
- **Parameters:**
  - `{manga_ID}`: Manga ID.
- **Response:** Returns manga details.

---

Thanks for exploring the Manga API! Feel free to follow for updates and improvements. 😊
