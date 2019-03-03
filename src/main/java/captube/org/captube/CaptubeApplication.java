package captube.org.captube;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.core.io.ResourceLoader;

@SpringBootApplication
public class CaptubeApplication extends SpringBootServletInitializer {
    public static void main(String[] args) {
        SpringApplication.run(CaptubeApplication.class, args);
    }
}

