import controller.Controller;
import repository.InMemoryRepository;
import repository.RepositoryInterface;
import view.CUI;
import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        RepositoryInterface repository = new InMemoryRepository();
        Controller controller = new Controller(repository);
        CUI cui = new CUI(scanner, controller);
        cui.run();
    }
}

/*
9. La o conferinta participa profesori, studenti si
specialisti din industrie. Sa se afiseze toti participantii
care au prezentat o lucrare.
 */