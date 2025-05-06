package project.recommendations.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import project.recommendations.model.Reminder;

import java.util.List;
import java.util.UUID;

public interface ReminderRepository extends JpaRepository<Reminder, UUID> {
    List<Reminder> findByPetId(UUID petId);
}