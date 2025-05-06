package com.example.community_service.service;

import com.example.community_service.model.ForumPost;
import com.example.community_service.repository.ForumPostRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class ForumPostService {
    private final ForumPostRepository forumPostRepository;
    private final ToxicCommentDetectorService toxicCommentDetectorService;

    public ForumPostService(ForumPostRepository forumPostRepository, ToxicCommentDetectorService toxicCommentDetectorService) {
        this.forumPostRepository = forumPostRepository;
        this.toxicCommentDetectorService = toxicCommentDetectorService;
    }

    public ForumPost createPost(ForumPost post) {
        if (toxicCommentDetectorService.isToxic(post.getContent())) {
            throw new IllegalArgumentException("Комментарий содержит неприемлемые выражения");
        }
        post.setCreatedAt(LocalDateTime.now());
        return forumPostRepository.save(post);
    }

    public List<ForumPost> getAllPosts() {
        return forumPostRepository.findAll();
    }

    public void deletePost(UUID id) {
        forumPostRepository.deleteById(id);
    }
}
