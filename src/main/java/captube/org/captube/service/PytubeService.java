package captube.org.captube.service;

import captube.org.captube.custom.CaptubeImage;
import ch.qos.logback.core.util.FileUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.*;

@Service
public class PytubeService {


    @Autowired
    private ResourceLoader resourceLoader;

    private static final String DEFAULT_LANGUAGE = "en";
    private static final String PYTUBE_SCRIPT_PATH =  System.getProperty("user.dir") +"/pytube/get_youtube.py";
    private static final String PYTUBE_RESOURCE_PATH = "pytube";
    private static final String PYTUBE_COPY_PATH = System.getProperty("user.dir") + "/pytube";

    @PostConstruct
    public void onPostConstruct() throws IOException {
        File pytubeFile = new File(PYTUBE_SCRIPT_PATH);
        if (!pytubeFile.exists()) {
            File pytubeDir = new File(PYTUBE_COPY_PATH);
            if (!pytubeDir.exists())
                pytubeDir.mkdirs();
            File pytubeResourceFile = new ClassPathResource(PYTUBE_RESOURCE_PATH).getFile();
            File[] resourceFiles = pytubeResourceFile.listFiles();

            for (File resourceFile : resourceFiles) {
                InputStream is = new FileInputStream(resourceFile);
                OutputStream os = new FileOutputStream(new File(PYTUBE_COPY_PATH + File.separator + resourceFile.getName()));

                byte[] buffer = new byte[1024];
                int read = 0;
                while ((read = is.read(buffer)) > 0) {
                    os.write(buffer, 0, read);
                }
                is.close();
                os.close();
            }
        }

    }

    public CaptubeImage[] getImages(String url) {
        CaptubeImage[] images = null;
        getImages(url, DEFAULT_LANGUAGE, false);
        return images;
    }

    public CaptubeImage[] getImages(String url, String language, boolean isNosub) {
        CaptubeImage[] images = null;
        Process captubeProcess = Runtime.getRuntime().exec()
        return images;
    }
}
