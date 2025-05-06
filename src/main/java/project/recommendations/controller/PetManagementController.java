package project.recommendations.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import project.recommendations.model.PetProfile;
import project.recommendations.model.Recommendation;
import project.recommendations.model.Reminder;
import project.recommendations.service.PetManagementService;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/pet")
public class PetManagementController {

    private final PetManagementService service;

    public PetManagementController(PetManagementService service) {
        this.service = service;
    }

    @PostMapping("/profile")
    public ResponseEntity<PetProfile> createProfile(@RequestBody PetProfile profile) {
        return ResponseEntity.ok(service.createPetProfile(profile));
    }

    @GetMapping("/profiles")
    public ResponseEntity<List<PetProfile>> getProfiles() {
        return ResponseEntity.ok(service.getAllPetProfiles());
    }

    @PostMapping("/recommendation")
    public ResponseEntity<Recommendation> createRecommendation(@RequestBody Recommendation recommendation) {
        return ResponseEntity.ok(service.createRecommendation(recommendation));
    }

    @GetMapping("/recommendations")
    public ResponseEntity<List<Recommendation>> getAllRecommendations() {
        return ResponseEntity.ok(service.getAllRecommendations());
    }

    @GetMapping("/{petId}/recommendations")
    public ResponseEntity<List<Recommendation>> getRecommendationsByPetId(@PathVariable UUID petId) {
        return ResponseEntity.ok(service.getRecommendationsByPetId(petId));
    }

    @PostMapping("/reminder")
    public ResponseEntity<Reminder> createReminder(@RequestBody Reminder reminder) {
        return ResponseEntity.ok(service.createReminder(reminder));
    }

    @GetMapping("/reminders")
    public ResponseEntity<List<Reminder>> getAllReminders() {
        return ResponseEntity.ok(service.getAllReminders());
    }

    @GetMapping("/{petId}/reminders")
    public ResponseEntity<List<Reminder>> getRemindersByPetId(@PathVariable UUID petId) {
        return ResponseEntity.ok(service.getRemindersByPetId(petId));
    }
}