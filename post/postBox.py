from post.models import Post, Image

class PostBox:
    #constructor
    def __init__(self, thumbnail, post, url):
        self.thumbnail = thumbnail
        self.post = post
        self.url = url

    #easy combine
    @staticmethod
    def easyCombine(posts, linkType):
        #combine posts with their respective images
        postBoxes = []
        for post in posts:
            postImages = Image.objects.filter(post=post.pk)[:1]

            if postImages:
                thumbnail = postImages[0]
            else:
                thumbnail = None

            aPost = PostBox(thumbnail, post, f"{linkType}{post.pk}")
            postBoxes.append(aPost)
        
        return postBoxes