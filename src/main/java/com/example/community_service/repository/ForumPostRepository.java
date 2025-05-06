package com.example.community_service.repository;

import com.example.community_service.model.ForumPost;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface ForumPostRepository extends JpaRepository<ForumPost, UUID> {
}

