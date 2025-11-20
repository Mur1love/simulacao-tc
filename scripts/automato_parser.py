import re
import xml.etree.ElementTree as ET


class State:
    def __init__(self, id, name, is_initial=False, is_final=False):
        self.id = id
        self.name = name
        self.is_initial = is_initial
        self.is_final = is_final


class Transition:
    def __init__(self, from_state, to_state, read_symbol):
        self.from_state = from_state
        self.to_state = to_state
        self.raw_read_symbol = read_symbol  # Keep the original for debugging if needed
        # Compile the read_symbol as a regex pattern
        # Handle epsilon transitions (empty string or None)
        if read_symbol is None or read_symbol == "":
            self.compiled_pattern = None  # Represents an epsilon transition
        else:
            # Pre-process read_symbol to handle specific regex parsing quirks from JFLAP.
            # Specifically, escape the hyphen if it creates a 'bad character range'
            # in a character class, e.g., '_-?' in JFLAP needs to be '_\\-?' for Python re.
            processed_read_symbol = read_symbol
            if processed_read_symbol.startswith("[") and processed_read_symbol.endswith(
                "]"
            ):
                # This is a targeted fix for the 'bad character range _-?' error.
                # It escapes the hyphen specifically when it appears between '_' and '?'.
                processed_read_symbol = processed_read_symbol.replace("_-?", "_\\-?")

            self.compiled_pattern = re.compile(processed_read_symbol)


class Automaton:
    def __init__(self):
        self.states = {}
        self.transitions = []
        self.initial_state = None
        self.final_states = []

    def add_state(self, state):
        self.states[state.id] = state
        if state.is_initial:
            self.initial_state = state
        if state.is_final:
            self.final_states.append(state)

    def add_transition(self, transition):
        self.transitions.append(transition)

    def accepts(self, word):
        if not self.initial_state:
            return False

        current_states = {self.initial_state.id}

        for symbol in word:
            next_states = set()
            for current_state_id in current_states:
                for transition in self.transitions:
                    # Check if transition is from current state
                    if transition.from_state == current_state_id:
                        # For non-epsilon transitions, match the symbol against the compiled pattern
                        if transition.compiled_pattern is not None:
                            if transition.compiled_pattern.fullmatch(symbol):
                                next_states.add(transition.to_state)
                        # Note: This 'accepts' method does not explicitly handle epsilon transitions (read_symbol == None)
                        # in a way that allows state changes without consuming a symbol.
                        # For DFAs, this is usually not an issue as they are defined without epsilons,
                        # or epsilons are removed during construction.
            current_states = next_states
            if not current_states:
                return False  # No possible transitions for the current symbol

        # Check if any of the current states are final states
        for state_id in current_states:
            if state_id in [s.id for s in self.final_states]:
                return True
        return False


def parse_jff(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    automaton = Automaton()

    # Parse states
    for state_elem in root.findall(".//state"):
        id = state_elem.get("id")
        name = state_elem.get("name")
        is_initial = state_elem.find("initial") is not None
        is_final = state_elem.find("final") is not None
        automaton.add_state(State(id, name, is_initial, is_final))

    # Parse transitions
    for transition_elem in root.findall(".//transition"):
        from_state = transition_elem.find("from").text
        to_state = transition_elem.find("to").text
        read_symbol_elem = transition_elem.find("read")
        # If <read/> is empty, .text is None. We want an empty string for epsilon.
        read_symbol = read_symbol_elem.text if read_symbol_elem is not None else ""

        automaton.add_transition(Transition(from_state, to_state, read_symbol))

    return automaton


if __name__ == "__main__":
    # Exemplo de uso
    try:
        # Assumindo que você tem um arquivo forte.jff no diretório automatos
        automaton = parse_jff("../automatos/forte.jff")
        print("Autômato carregado com sucesso!")

        # Testando algumas senhas
        print(f"'Senha@123' é aceita: {automaton.accepts('Senha@123')}")
        print(f"'abc' é aceita: {automaton.accepts('abc')}")
        print(
            f"'Senha123' é aceita: {automaton.accepts('Senha123')}"
        )  # Should be false for forte (missing symbol)
        print(
            f"'Abcdefg1!' é aceita: {automaton.accepts('Abcdefg1!')}"
        )  # Should be true if it has all requirements
        print(f"'fraca1234' é aceita: {automaton.accepts('fraca1234')}")

    except FileNotFoundError:
        print(
            "Arquivo JFLAP não encontrado. Certifique-se de que o caminho está correto."
        )
    except Exception as e:
        print(f"Ocorreu um erro ao parsear o arquivo JFLAP: {e}")
