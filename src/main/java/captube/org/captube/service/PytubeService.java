package captube.org.captube.service;

import captube.org.captube.custom.CaptubeImage;
import ch.qos.logback.core.util.FileUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.*;
import java.util.concurrent.TimeUnit;

@Service
public class PytubeService {

    private Logger logger = LoggerFactory.getLogger(PytubeService.class);
    @Autowired
    private ResourceLoader resourceLoader;

    private static final String DEFAULT_LANGUAGE = "en";
    private static final String PYTUBE_SCRIPT_PATH = System.getProperty("user.dir") + File.separator + "pytube"
            + File.separator + "get_youtube.py";
    private static final String CAPTURE_RESULT_PATH = System.getProperty("user.dir") + File.separator + "pytube"
            + File.separator + "imgs";
    private static final String PREFIX_IMG = "downloaded_video";
    private static final int CAPTURE_TIMOUT = 15 * 60 * 1000;


    public CaptubeImage[] getImages(String url) throws Exception, IOException, InterruptedException {
        CaptubeImage[] images = null;
        getImages(url, DEFAULT_LANGUAGE, false);
        return images;
    }

    public CaptubeImage[] getImages
            (String url, String language, boolean isNosub) throws Exception, IOException, InterruptedException {

        CaptubeImage[] images = null;

        Process captubeProcess = Runtime.getRuntime().exec(
                isNosub ?
                        new String[]{"python", PYTUBE_SCRIPT_PATH, "-u", url, "-l", language} :
                        new String[]{"python", PYTUBE_SCRIPT_PATH, "-u", url, "-l", language, "--no-sub"});
        captubeProcess.waitFor(CAPTURE_TIMOUT, TimeUnit.MILLISECONDS);
        if (captubeProcess.exitValue() == 0) {
            final BufferedReader reader = new BufferedReader(
                    new InputStreamReader(captubeProcess.getInputStream()));
            String line = null;
            while ((line = reader.readLine()) != null) {
                logger.info(line);
            }
            reader.close();

            File resultDir = new File(CAPTURE_RESULT_PATH);
            File[] imgFiles = resultDir.listFiles();

            for (File imgFile : imgFiles) {
                logger.info(imgFile.getName());
            }

        } else {
            final BufferedReader reader = new BufferedReader(
                    new InputStreamReader(captubeProcess.getErrorStream()));
            String line = null;
            while ((line = reader.readLine()) != null) {
                logger.error(line);
            }
            reader.close();
            throw new Exception("Failed to capture youtube");
        }
        return images;
    }
}
