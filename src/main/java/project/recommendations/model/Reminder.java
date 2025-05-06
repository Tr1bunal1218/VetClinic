package project.recommendations.model;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "reminder")
public class Reminder {

    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "pet_id")
    private UUID petId;

    private String type;

    @Column(name = "remind_date")
    private LocalDate remindDate;

}
