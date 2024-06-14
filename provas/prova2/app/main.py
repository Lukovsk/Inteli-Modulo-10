from fastapi import FastAPI
from logs import log_warning, log_info, log_critical, log_debug, log_error


app = FastAPI()

blog_posts = []


class BlogPost:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

    def __str__(self) -> str:
        return f"{self.id} - {self.title} - {self.content}"

    def toJson(self):
        return {"id": self.id, "title": self.title, "content": self.content}


from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    content: str


@app.post("/blog")
def create_blog_post(data: Blog):
    log_debug("Creating blog post")
    try:
        blog_posts.append(BlogPost(len(blog_posts), data.title, data.content))
        log_info("Blog post created")
        return {"status": "sucess"}, 201
    except KeyError:
        log_warning("Blog post creation")
        return ({"error": "Invalid request"}), 400
    except Exception as e:
        log_critical("Blog post creation")
        return ({"error": str(e)}), 500


@app.get("/blog")
def get_blog_posts():
    log_info("Getting blog posts")
    return {"posts": [blog.toJson() for blog in blog_posts]}, 200


@app.get("/blog/{id}")
def get_blog_post(id):
    log_info("Getting blog post")
    for post in blog_posts:
        if post.id == id:
            return ({"post": post.__dict__}), 200
    log_error("Getting blog post")
    return ({"error": "Post not found"}), 404


@app.delete("/blog/{id}")
def delete_blog_post(id):
    log_info("Deleting blog post")
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            return ({"status": "sucess"}), 200
    log_error("Blog post not found")
    return ({"error": "Post not found"}), 404


@app.put("/blog/{id}")
def update_blog_post(id: int, body: Blog):
    log_info("Updating blog post")
    try:
        data = body.get_json()
        for post in blog_posts:
            if post.id == id:
                post.title = data.title
                post.content = data.content
                return ({"status": "sucess"}), 200
        log_warning("Post not found to update")
        return ({"error": "Post not found"}), 404
    except KeyError:
        log_error("Post not found to update")
        return ({"error": "Invalid request"}), 400
    except Exception as e:
        log_critical("Unknown error deleting post")
        return ({"error": str(e)}), 500


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
