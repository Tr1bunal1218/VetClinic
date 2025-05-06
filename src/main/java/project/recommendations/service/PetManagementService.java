package project.recommendations.service;

import org.springframework.stereotype.Service;
import project.recommendations.model.PetProfile;
import project.recommendations.model.Recommendation;
import project.recommendations.model.Reminder;
import project.recommendations.repository.PetProfileRepository;
import project.recommendations.repository.RecommendationRepository;
import project.recommendations.repository.ReminderRepository;

import java.util.List;
import java.util.UUID;

@Service
public class PetManagementService {

    private final PetProfileRepository petProfileRepository;
    private final RecommendationRepository recommendationRepository;
    private final ReminderRepository reminderRepository;

    public PetManagementService(PetProfileRepository petProfileRepository,
                                RecommendationRepository recommendationRepository,
                                ReminderRepository reminderRepository) {
        this.petProfileRepository = petProfileRepository;
        this.recommendationRepository = recommendationRepository;
        this.reminderRepository = reminderRepository;
    }

    // === PetProfile ===
    public PetProfile createPetProfile(PetProfile profile) {
        return petProfileRepository.save(profile);
    }

    public List<PetProfile> getAllPetProfiles() {
        return petProfileRepository.findAll();
    }

    // === Recommendation ===
    public Recommendation createRecommendation(Recommendation recommendation) {
        return recommendationRepository.save(recommendation);
    }

    public List<Recommendation> getAllRecommendations() {
        return recommendationRepository.findAll();
    }

    public List<Recommendation> getRecommendationsByPetId(UUID petId) {
        return recommendationRepository.findByPetId(petId);
    }

    // === Reminder ===
    public Reminder createReminder(Reminder reminder) {
        return reminderRepository.save(reminder);
    }

    public List<Reminder> getAllReminders() {
        return reminderRepository.findAll();
    }

    public List<Reminder> getRemindersByPetId(UUID petId) {
        return reminderRepository.findByPetId(petId);
    }
}