
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.*;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Optional;


public class UserTest {
    private Connection connection;


    public UserTest() throws SQLException {
        this.connection = DriverManager.getConnection("jdbc:sqlite::memory:");
    }

    @After
    public void tearDown() throws Exception {
        Statement s = connection.createStatement();
        s.execute("drop table users");
        s.close();
    }

    @Test
    public void testSingleUserCreation() {
        UserDao ud = new UserDao(connection);
        ud.createUser("jill@example.com", "hunter1111");

        Optional<User> u = ud.getUser("jill@example.com");

        assertTrue(u.isPresent());
        User user = u.get();
        assertEquals("jill@example.com", user.getEmail());


        Optional<User> u2 = ud.getUser("jill@example.com");

        assertTrue(u2.isPresent());
        User sameUser = u2.get();
        assertEquals(user, sameUser);
    }

    @Test
    public void testAuthentication() {
        UserDao ud = new UserDao(connection);
        ud.createUser("jill@example.com", "abcdefg");
        Optional<User> u = ud.getAuthenticatedUser("jill@example.com", "abcdefg");

        assertTrue(u.isPresent());
        assertEquals("jill@example.com", u.get().getEmail());

        u = ud.getAuthenticatedUser("jill@example.com", "wrong");
        assertTrue(u.isEmpty());

        u = ud.getAuthenticatedUser("bill@example.com", "abcdefg");
        assertTrue(u.isEmpty());

        u = ud.getAuthenticatedUser("bill@example.com", "wrong");
        assertTrue(u.isEmpty());
    }

    @Test
    public void testMultipleUserCreation() throws SQLException {
        UserDao ud = new UserDao(connection);
        ud.createUser("jill@example.com", "hunter1111");
        ud.createUser("jack@example.com", "bunter1112");

        Optional<User> u = ud.getUser("jill@example.com");

        assertTrue(u.isPresent());
        User user = u.get();
        assertEquals("jill@example.com", user.getEmail());

        Optional<User> u2 = ud.getUser("jack@example.com");
        assertTrue(u2.isPresent());
        User user2 = u2.get();

        assertEquals("jack@example.com", user2.getEmail());

        u = ud.getUser("jill@example.com");
        u2 = ud.getUser("jack@example.com");

        assertTrue(u.isPresent());
        assertTrue(u2.isPresent());

        assertEquals(user, u.get());
        assertEquals(user2, u2.get());
    }

}