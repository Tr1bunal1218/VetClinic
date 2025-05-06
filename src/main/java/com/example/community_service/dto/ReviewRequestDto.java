package com.example.community_service.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ReviewRequestDto {
    public String clinicName;
    public String doctorName;
    public Integer rating;
    public String comment;
    public String user;
}

