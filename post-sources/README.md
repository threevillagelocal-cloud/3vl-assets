# Designed BD post backups (source of truth)

BD's built-in post editor (Froala) strips <style> blocks, <section>/<figure> wrappers and captions
whenever a post is opened and saved in the admin. It happened to Karing for Kids (post 252) on 9/23/2026.

These files are the exact post_content of each designed post as last published through the API.
Restore with the BD API (PUT /api/v2/data_posts/update, post_id + post_content), then refresh the site cache.
Never edit these posts in the BD admin editor.
