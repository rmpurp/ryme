# Ryme
A Lean and Modern Blogging Engine

Ryme is a blogging engine based on Node.js on the backend and React.js in the frontend. The frontend is designed as a single-page app with URL routing through the React Router framework. The frontend is easily customizable by virtue of being composed of modular React components.

## Markdown files
There are two special fields that you have to put in the Markdown files:
```
@@Title=<Title>
@@Date=YYYY-MM-DD
```

(Note that `<Title>` should not have the `<>`: i.e. a valid header would be something like
```
@@Title=2020 Vision!
@@Date=2020-01-01
```

You can specify a ISO-8601 date including the time to order posts on the same day. Make sure the date you enter matches which folder the file is put into.

## Admin Panel (Beta)
The Admin panel is hosted at /admin and is currently authenticated using HTTP basic authentication (subject to change). Change the username and password in the `server/server_config.js` file. The config file expects the password to be hashed using bcrypt so you will need to bcrypt your password manually. The admin panel allows you to delete old posts, create new posts, and override posts (by creating a new post with the same date and slug). 

## Usage
1. Install node modules using `npm install`.
2. Compile the frontend and the backend using `npm run build-all`.
3. Put Markdown posts into the posts directory using the format `posts/YYYY/MM/DD/title.md`. 

## Website Structure
The root of the website shows the most recent 10 days that have posts. Permalinks are automatically generated for each post under the url `<root.tld>/YYYY/MM/DD/slug` where `slug` is the filename of the Markdown file without the `.md` extension. Each month's post can be found under `<root.tld>/YYYY/MM` and the archive that contains links to all of the month pages is `<root.tld>/archives`.
