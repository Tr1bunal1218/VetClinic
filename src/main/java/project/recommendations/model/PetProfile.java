package project.recommendations.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "pet_profile")
public class PetProfile {

    @Id
    @GeneratedValue
    private UUID id;

    private String name;
    private String breed;

    @Column(name = "has_allergy")
    private Boolean hasAllergy;

    // getters and setters
}
