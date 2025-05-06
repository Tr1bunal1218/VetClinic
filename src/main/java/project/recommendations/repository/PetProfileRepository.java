package project.recommendations.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import project.recommendations.model.PetProfile;

import java.util.UUID;

public interface PetProfileRepository extends JpaRepository<PetProfile, UUID> {
}
