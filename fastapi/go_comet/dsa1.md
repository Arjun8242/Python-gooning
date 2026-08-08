Recommender System
You are building a Text Recommender System that predicts what word the user will be typing based on the words he has used before.

According to the algorithm, your system should recommend that word which is most frequently used by the user before.

You are given a dictionary containing various words(may be repeated) and an integer k. Recommend top k words.

Note: If two words occur the same number of times, then the lexographically smaller one should be recommended first.

Input Format
First line contains an two space separated integers n k which is the number of words in the user's dictionary and the number of words you need to recommend.

Next n contain a string corresponding to a word.

Output Format
Complete the function RecommendWords() which returns an array of size k containing strings

Example 1
Input

6 2
i
love
acciojob
i
love
coding
Output

i
love
Explanation

Words with their counts are: {[i, 2], [love, 2], [acciojob, 1], [coding, 1]}

Since k == 2, we recommend words {i, love}

Example 2
Input

6 3
burger
is
tasty
burger
tasty
tasty
Output

tasty
burger
is
Constraints
1 <= wordDict.size() <= 500

1 <= wordDict[i] <= 10





import java.util.*;

public class Main {

    public static List<String> recommendWords(List<String> wordDict, int k) {

        // Step 1: Count frequency of each word
        HashMap<String, Integer> freq = new HashMap<>();

        for (String word : wordDict) {
            freq.put(word, freq.getOrDefault(word, 0) + 1);
        }

        // Step 2: Store unique words
        List<String> words = new ArrayList<>(freq.keySet());

        // Step 3: Sort
        Collections.sort(words, (a, b) -> {

            // Higher frequency first
            if (!freq.get(a).equals(freq.get(b))) {
                return freq.get(b) - freq.get(a);
            }

            // Same frequency -> lexicographically smaller first
            return a.compareTo(b);
        });

        // Step 4: Return first k words
        return words.subList(0, k);
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int k = sc.nextInt();

        List<String> wordDict = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            wordDict.add(sc.next());
        }

        List<String> ans = recommendWords(wordDict, k);

        for (String word : ans) {
            System.out.println(word);
        }
    }
}