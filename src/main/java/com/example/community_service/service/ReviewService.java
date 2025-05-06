package com.example.community_service.service;

import com.example.community_service.exception.ToxicCommentException;
import com.example.community_service.model.Review;
import com.example.community_service.repository.ReviewRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class ReviewService {
    private final ReviewRepository reviewRepository;
    private final ToxicCommentDetectorService toxicCommentDetectorService;

    public ReviewService(ReviewRepository reviewRepository, ToxicCommentDetectorService toxicCommentDetectorService) {
        this.reviewRepository = reviewRepository;
        this.toxicCommentDetectorService = toxicCommentDetectorService;
    }

    public Review createReview(Review review) {
        if (toxicCommentDetectorService.isToxic(review.getComment())) {
            throw new ToxicCommentException("Ваш отзыв содержит нецензурные выражения и не может быть опубликован.");
        }
        review.setCreatedAt(LocalDateTime.now());
        return reviewRepository.save(review);
    }

    public List<Review> getAllReviews() {
        return reviewRepository.findAll();
    }

    public void deleteReview(UUID id) {
        reviewRepository.deleteById(id);
    }
}

