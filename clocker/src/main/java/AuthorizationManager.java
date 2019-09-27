import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Base64;
import java.security.SecureRandom;
import java.util.Date;

public class AuthorizationManager {
    private Connection connection;
    public AuthorizationManager(Connection c) {
        this.connection = c;

        try {
            Statement statement = connection.createStatement();
            statement.executeUpdate("create table if not exists auth_tokens (token text PRIMARY KEY, uid integer, creation_date integer, expiration_date integer)");
            statement.close();
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }
    }

    public String getAuthorizationToken(int userId) {
        Date currentDate = new Date();
        Date expirationDate = new Date(currentDate.getTime() + 3600 * 24 * 30);
        return getAuthorizationToken(userId, new Date(), expirationDate);
    }

    public String getAuthorizationToken(int userId, Date creationDate, Date expirationDate) {
        SecureRandom random = new SecureRandom();
        byte[] token = new byte[32];
        random.nextBytes(token);
        String base64Encoded = Base64.getEncoder().encodeToString(token);
        try {
            PreparedStatement ps = connection.prepareStatement("insert into auth_tokens values (?, ?, ?, ?)");
            ps.setString(1, base64Encoded);
            ps.setInt(2, userId); //TODO make userids longs
            ps.setLong(3, creationDate.getTime());
            ps.setLong(4, expirationDate.getTime());
            ps.execute();
            return base64Encoded;
        } catch (SQLException e) {
            throw new DaoException(e.getMessage()); //TODO: change exception or refactor?
        }
    }
}
