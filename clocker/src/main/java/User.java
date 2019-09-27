import java.util.Objects;

public class User {
    private String email;
    private String salt;
    private String hash;
    private int id;

    public String getEmail() {
        return email;
    }

    public String getHash() {
        return hash;
    }

    public int getId() {
        return id;
    }

    @Override
    public String toString() {
        return "User{" +
                "email='" + email + '\'' +
                ", salt='" + salt + '\'' +
                ", hash='" + hash + '\'' +
                ", id=" + id +
                '}';
    }

    public String getSalt() {
        return salt;
    }

    public User(String email, String hash, String salt, int id) {
        this.email = email;
        this.salt = salt;
        this.hash = hash;
        this.id = id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User)) return false;
        User user = (User) o;
        return id == user.id &&
                email.equals(user.email) &&
                hash.equals(user.hash);
    }

    @Override
    public int hashCode() {
        return Objects.hash(email, hash, id);
    }
}
