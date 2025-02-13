package org.dutylist.users.security;

import io.github.cdimascio.dotenv.Dotenv;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.io.InputStream;

@Configuration
public class FirebaseConfig {

    @Bean
    public FirebaseApp firebaseApp() throws IOException {
        Dotenv dotenv = Dotenv.load();
        InputStream serviceAccount = getClass().getClassLoader().getResourceAsStream("firebase-service-account.json");

        if(serviceAccount == null) {
            throw new RuntimeException("Could not find service account file");
        }

        FirebaseOptions options = FirebaseOptions.builder()
                .setCredentials(GoogleCredentials.fromStream(serviceAccount))
                .setDatabaseUrl(dotenv.get("FIREBASE_REALTIME_DATABASE_URL"))
                .build();

        if (FirebaseApp.getApps().isEmpty()) {
            return FirebaseApp.initializeApp(options);
        } else {
            return FirebaseApp.getInstance();
        }
    }
}
