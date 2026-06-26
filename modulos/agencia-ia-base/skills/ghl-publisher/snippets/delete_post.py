"""
delete_post.py — Deletar post no CRM Funnels.

⚠️ Atenção: deletar um sub-post NÃO deleta o parent post automaticamente.
Se o parent ainda tem scheduleDate futuro, ele pode recriar sub-posts.
Para cancelar de verdade, deletar o parent (post sem parentPostId).
"""
import sys
from _common import LOC, http_request


def delete_post(post_id: str) -> dict:
    return http_request("DELETE", f"/social-media-posting/{LOC}/posts/{post_id}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python delete_post.py <postId> [<postId> ...]")
        sys.exit(1)
    for pid in sys.argv[1:]:
        try:
            res = delete_post(pid)
            print(f"  ✅ {pid}: {res.get('message', 'deleted')}")
        except Exception as e:
            print(f"  ❌ {pid}: {e}")
