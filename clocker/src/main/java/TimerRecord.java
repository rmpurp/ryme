import java.util.Date;
import java.util.Objects;

public class TimerRecord {
    private int userId;
    private Date start;
    private Date end;
    private String label;

    public TimerRecord(int userId, Date start, Date end, String label) {
        this.userId = userId;
        this.start = start;
        this.end = end;
        this.label = label;
    }

    @Override
    public String toString() {
        return "TimerRecord{" +
                "userId=" + userId +
                ", start=" + start +
                ", end=" + end +
                ", label='" + label + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof TimerRecord)) return false;
        TimerRecord that = (TimerRecord) o;
        return getUserId() == that.getUserId() &&
                getStart().equals(that.getStart()) &&
                getEnd().equals(that.getEnd()) &&
                getLabel().equals(that.getLabel());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getUserId(), getStart(), getEnd(), getLabel());
    }

    public int getUserId() {
        return userId;
    }

    public Date getStart() {
        return start;
    }

    public Date getEnd() {
        return end;
    }

    public String getLabel() {
        return label;
    }
}
