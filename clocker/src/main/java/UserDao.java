import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.swing.text.html.Option;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Optional;

public class UserDao {
    private Connection connection;


    public UserDao(Connection connection) {
        this.connection = connection;
        try {
            Statement statement = connection.createStatement();
            statement.executeUpdate("create table if not exists users (email text unique, hash text, salt text, id integer PRIMARY KEY)");
            statement.close();
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }
    }

    public Optional<String> getAuthorizationToken(String email, String password) {
        Optional<User> optionalUser = getAuthenticatedUser(email, password);
        if (optionalUser.isEmpty()) {
            return Optional.empty();
        }

        AuthorizationManager authorizationManager = new AuthorizationManager(connection);
        String token = authorizationManager.getAuthorizationToken(optionalUser.get().getId());
        return Optional.of(token);
    }

    public Optional<User> getAuthenticatedUser(String email, String password) {
        Optional<User> optional = getUser(email);
        if (optional.isEmpty()) {
            return Optional.empty();
        }

        User u = optional.get();
        String calculatedHash = getHash(password, u.getSalt());
        if (u.getHash().equals(calculatedHash)) {
            return Optional.of(u);
        } else {
            return Optional.empty();
        }
    }

    public void createUser(String email, String password) {
        if (getUser(email).isPresent()) {
            throw new RuntimeException("TODO: handle me"); //TODO: handle dup emails
        }

        String salt = getSalt();
        String hash = getHash(password, salt);

        try {
            PreparedStatement ps = connection.prepareStatement("insert into users values (?, ?, ?, null)");
            ps.setString(1, email);
            ps.setString(2, hash);
            ps.setString(3, salt);
            ps.execute();
            ps.close();
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }
    }

    public static String getSalt() {
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[32];
        random.nextBytes(salt);
        return new String(salt);
    }


    public static String getHash(String password, String salt) {
        try {
            PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(), 65536, 256);
            SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
            return new String(factory.generateSecret(spec).getEncoded(), StandardCharsets.UTF_8);
        } catch (InvalidKeySpecException | NoSuchAlgorithmException e) {
            throw new DaoException(e.getMessage());
        }
    }


    public Optional<User> getUser(String email) {
        try {
            PreparedStatement ps = connection.prepareStatement("select hash, salt, id from users where email = ?");
            ps.setString(1, email);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                String hash = rs.getString("hash");
                String salt = rs.getString("salt");
                int id = rs.getInt("id");
                ps.close();
                return Optional.of(new User(email, hash, salt, id));
            } else {
                ps.close();
                return Optional.empty();
            }


        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }

    }


}
