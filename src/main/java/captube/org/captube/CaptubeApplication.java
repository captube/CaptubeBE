package captube.org.captube;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.io.ResourceLoader;

@SpringBootApplication
public class CaptubeApplication {
    public static void main(String[] args) {
        SpringApplication.run(CaptubeApplication.class, args);
    }
}

