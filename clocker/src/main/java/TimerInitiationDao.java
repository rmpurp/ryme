import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Date;
import java.util.Optional;

public class TimerInitiationDao {
    private Connection connection;

    public TimerInitiationDao(Connection connection) {
        this.connection = connection;
        try {
            Statement statement = connection.createStatement();
            statement.setQueryTimeout(30);
            statement.executeUpdate("create table if not exists timerinitiation (uid integer unique, start integer, label text, status integer)");
            statement.close();
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }
    }

    public boolean cancelTimerInitiation(int userId) {
        Optional<TimerInitiation> optional = getTimerInitiation(userId);
        if (optional.isEmpty()) {
            return false;
        }

        TimerInitiation ti = optional.get();
        if (ti.getStatus() != TimerInitiation.STARTED) {
            return false;
        }

        updateTimerInitiation(userId, ti.getStart(), ti.label(), TimerInitiation.CANCELLED);
        return true;
    }

    public boolean endTimerInitiation(int userId) {
        Optional<TimerInitiation> optional = getTimerInitiation(userId);
        if (optional.isEmpty()) {
            return false;
        }

        TimerInitiation ti = optional.get();
        if (ti.getStatus() != TimerInitiation.STARTED) {
            return false;
        }

        updateTimerInitiation(userId, ti.getStart(), ti.label(), TimerInitiation.ENDED);
        return true;
    }

    public boolean createTimerInitiation(int userId, Date start, String label) {
        Optional<TimerInitiation> optional = getTimerInitiation(userId);
        if (optional.isPresent() && optional.get().getStatus() == TimerInitiation.STARTED) {
            return false;
        }

        return updateTimerInitiation(userId, start, label, TimerInitiation.STARTED);
    }

    public boolean updateTimerInitiation(int userId, Date start, String label, int status) {

        try {
            PreparedStatement ps = connection.prepareStatement("insert or replace into timerinitiation values (?, ?, ?, ?)");
            ps.setInt(1, userId);
            ps.setLong(2, start.getTime());
            ps.setString(3, label);
            ps.setInt(4, status);
            ps.execute();
            ps.close();
            return true;

        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }

    }

    public Optional<TimerInitiation> getTimerInitiation(int userId) {
        try {
            PreparedStatement ps = connection.prepareStatement("select start, status, label from timerinitiation where uid = ?");
            ps.setInt(1, userId);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                int status = rs.getInt("status");
                long milliseconds = rs.getLong("start");
                String label = rs.getString("label");
                Date date = new Date(milliseconds);
                ps.close();
                return Optional.of(new TimerInitiation(userId, label, date, status));
            } else {
                ps.close();
                return Optional.empty();
            }
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }

    }
}
