package project.recommendations.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import project.recommendations.model.Recommendation;

import java.util.List;
import java.util.UUID;

public interface RecommendationRepository extends JpaRepository<Recommendation, UUID> {
    List<Recommendation> findByPetId(UUID petId);
}
