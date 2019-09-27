import java.util.Date;

public class TimerInitiation {
    public static final int STARTED = 0;
    public static final int ENDED = 1;
    public static final int CANCELLED = 2;

    private int userId;
    private Date start;
    private int status;
    private String label;

    @Override
    public String toString() {
        return "TimerInitiation{" +
                "userId=" + userId +
                ", start=" + start +
                ", status=" + status +
                ", label='" + label + '\'' +
                '}';
    }

    public TimerInitiation(int userId, String label, Date start, int status) {
        this.userId = userId;
        this.start = start;
        this.label = label;
        this.status = status;
        getUserId()
    }

    public int getUserId() {
        return userId;
    }

    public Date getStart() {
        return start;
    }

    public int getStatus() {
        return status;
    }

    public String label() {
        return label;
    }
}
