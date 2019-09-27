import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.Base64;
import java.util.Date;

import static spark.Spark.get;

public class Main {
    public static void main(String[] args) throws SQLException {

        get("/hello", (req, res) -> {
            String authHeader = req.headers("Authorization");
            if (res == null) {
                res.header("WWW-Authenticate", "Basic realm=\"Access to the staging site\", charset=\"UTF-8\"");
                System.out.println(authHeader);
                res.status(401);
                return "yesn't";
            }
            String base64Credentials = authHeader.substring("Basic".length()).trim();
            byte[] credDecoded = Base64.getDecoder().decode(base64Credentials);
            String credentials = new String(credDecoded, StandardCharsets.UTF_8);
            // credentials = username:password
            final String[] values = credentials.split(":", 2);
            System.out.println(Arrays.toString(values));
            return "ok";
        });

        Connection connection = DriverManager.getConnection("jdbc:sqlite:test.db");

        connection.createStatement().execute("drop table if exists users");
        connection.createStatement().execute("drop table if exists timerinitiation");
        connection.createStatement().execute("drop table if exists timerrecord");

        UserDao userDao = new UserDao(connection);

        if (userDao.getUser("bob@bob.com").isEmpty()) {
            userDao.createUser("bob@bob.com", "hunterasdf7");
        }

        User bob = userDao.getUser("bob@bob.com").get();

        TimerInitiationDao tiDao = new TimerInitiationDao(connection);

        tiDao.createTimerInitiation(bob.getId(), new Date(), "starto");

        System.out.println(tiDao.getTimerInitiation(bob.getId()));

        TimerRecordDao trd = new TimerRecordDao(connection);

        trd.createTimerRecord(bob.getId(), new Date());

        tiDao.createTimerInitiation(bob.getId(), new Date(), "cancelme");
        tiDao.cancelTimerInitiation(bob.getId());

        System.out.println(trd.getTimerRecords(bob.getId()));
    }
}

