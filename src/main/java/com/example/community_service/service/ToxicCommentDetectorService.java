package com.example.community_service.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Arrays;
import java.util.List;

@Service
public class ToxicCommentDetectorService {

    @Value("${huggingface.api.token}")
    private String apiToken;

    private static final String API_URL = "https://api-inference.huggingface.co/models/cointegrated/rubert-tiny-toxicity";


    // Чёрный список — можешь расширить
    private static final List<String> BLACKLIST = Arrays.asList(
            // Английские
            "idiot", "stupid", "dumb", "ugly", "kill yourself", "hate", "bastard",
            "fool", "loser", "fat", "nigger", "faggot", "retard", "bitch", "asshole", "bastard", "cunt",
            "motherfucker", "whore", "slut", "dickhead", "prick", "pussy", "cock", "shit", "fuck", "fucking", "fucked",
            "bitchass", "asswipe", "douchebag", "twat", "wanker", "scumbag", "piece of shit", "freaking", "cockhead",
            "shithead", "craphead", "dick", "jackass", "assclown", "bastard", "loser", "moron", "imbecile", "douche", "skank",

            // Русские
            "идиот", "тупой", "дурак", "урод", "жирный", "дебил", "ненавижу",
            "сдохни", "убью", "сука", "пидор", "гондон", "мудак", "мразь", "тварь", "гнида", "сволочь", "падла", "дура", "мерзавец",
            "залупа", "пизда", "еблан", "пидорас", "мразь", "дурачок", "на*уй", "блядь", "шлюха", "проститутка", "гандон", "гавно","говно",
            "обезьяна", "тварь", "долбоёб", "сучара","чмо", "поебень", "хер", "пиздец", "ебать", "блять", "ёбнутый",
            "трахать", "ебучий", "петушара", "отстой", "поебать", "ебло", "пиздануть", "педик", "сучий сын", "охуел", "нахер", "стервозина"
    );



    public boolean isToxic(String content) {
        String normalized = content.toLowerCase();

        // 1. Жёсткая фильтрация — если содержит запрещённое слово
        for (String badWord : BLACKLIST) {
            if (normalized.contains(badWord)) {
                return true;
            }
        }

        try {
            RestTemplate restTemplate = new RestTemplate();

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.setBearerAuth(apiToken);

            JSONObject body = new JSONObject();
            body.put("inputs", content);

            HttpEntity<String> entity = new HttpEntity<>(body.toString(), headers);

            ResponseEntity<String> response = restTemplate.postForEntity(API_URL, entity, String.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                JSONArray responseArray = new JSONArray(response.getBody());

                for (int i = 0; i < responseArray.length(); i++) {
                    JSONArray labels = responseArray.getJSONArray(i);
                    for (int j = 0; j < labels.length(); j++) {
                        JSONObject label = labels.getJSONObject(j);
                        String name = label.getString("label");
                        double score = label.getDouble("score");

                        // Можно расширить список категорий
                        if ((name.toLowerCase().contains("toxicity")
                                || name.toLowerCase().contains("insult")
                                || name.toLowerCase().contains("threat")
                                || name.toLowerCase().contains("obscene"))
                                && score >= 0.6) {
                            return true;
                        }
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return false;
    }
}
