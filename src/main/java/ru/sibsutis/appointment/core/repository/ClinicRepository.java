package ru.sibsutis.appointment.core.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.sibsutis.appointment.core.model.Clinic;

import java.util.UUID;

@Repository
public interface ClinicRepository extends JpaRepository<Clinic, UUID> {
}