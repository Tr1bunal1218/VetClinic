package project.recommendations.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "recommendation")
public class Recommendation {

    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "pet_id")
    private UUID petId;

    private String text;
    // getters and setters
}
