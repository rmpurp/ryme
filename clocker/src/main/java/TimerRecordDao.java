import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;

public class TimerRecordDao {
    private Connection connection;

    public TimerRecordDao(Connection connection) {
        this.connection = connection;

        try {
            Statement statement = connection.createStatement();
            statement.setQueryTimeout(30);
            statement.executeUpdate("create table if not exists timerrecord (uid integer, start integer, end integer, label text)");
            statement.close();
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }

    }

    public List<TimerRecord> getTimerRecords(int userId) {
        try {
            PreparedStatement ps = connection.prepareStatement("select * from timerrecord where uid = ?");
            ps.setInt(1, userId);
            List<TimerRecord> list = new ArrayList<>();
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                Date start = new Date(rs.getLong("start"));
                Date end = new Date(rs.getLong("end"));
                String label = rs.getString("label");
                list.add(new TimerRecord(userId, start, end, label));
            }
            ps.close();
            return list;
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }
    }

    public boolean createTimerRecord(int userId, Date end) {
        try {
            connection.setAutoCommit(false);
            TimerInitiationDao tid = new TimerInitiationDao(connection);
            Optional<TimerInitiation> optional = tid.getTimerInitiation(userId);
            if (optional.isEmpty()) {
                return false;
            }
            TimerInitiation ti = optional.get();
            if (ti.getStatus() != TimerInitiation.STARTED) {
                return false;
            }

            PreparedStatement ps = connection.prepareStatement("insert into timerrecord values (?, ?, ?, ?)");
            ps.setInt(1, userId);
            ps.setLong(2, ti.getStart().getTime());
            ps.setLong(3, end.getTime());
            ps.setString(4, ti.label());
            ps.execute();
            ps.close();

            tid.endTimerInitiation(userId);

            connection.commit();
            connection.setAutoCommit(true);
            return true;
        } catch (SQLException e) {
            throw new DaoException(e.getMessage());
        }
    }


}
