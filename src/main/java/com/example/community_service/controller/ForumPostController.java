package com.example.community_service.controller;

import com.example.community_service.model.ForumPost;
import com.example.community_service.service.ForumPostService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/forum")
public class ForumPostController {
    private final ForumPostService forumPostService;

    public ForumPostController(ForumPostService forumPostService) {
        this.forumPostService = forumPostService;
    }

    @PostMapping
    public ResponseEntity<ForumPost> createPost(@RequestBody ForumPost post) {
        return ResponseEntity.ok(forumPostService.createPost(post));
    }

    @GetMapping
    public ResponseEntity<List<ForumPost>> getAllPosts() {
        return ResponseEntity.ok(forumPostService.getAllPosts());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletePost(@PathVariable UUID id) {
        forumPostService.deletePost(id);
        return ResponseEntity.noContent().build();
    }
}
