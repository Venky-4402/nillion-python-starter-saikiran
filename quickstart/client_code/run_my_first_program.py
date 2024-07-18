from nada_dsl import *

def nada_main():
    # Define the parties for the users
    user_1 = Party(name="User 1 💉")
    user_2 = Party(name="User 2 💉")

    # Define secret inputs for the initial doses, vaccination requests, and cancellation requests
    initial_doses = SecretInteger(Input(name="initial_doses", party=user_1))  # Total doses available
    received_doses_user_1 = SecretInteger(Input(name="received_doses_user_1", party=user_1))
    canceled_doses_user_1 = SecretInteger(Input(name="canceled_doses_user_1", party=user_1))
    received_doses_user_2 = SecretInteger(Input(name="received_doses_user_2", party=user_2))
    canceled_doses_user_2 = SecretInteger(Input(name="canceled_doses_user_2", party=user_2))

    # Calculate the new dose allocation after vaccination requests
    doses_after_vaccination_user_1 = (initial_doses >= received_doses_user_1).if_else(
        initial_doses - received_doses_user_1,
        initial_doses
    )

    doses_after_vaccination_user_2 = (doses_after_vaccination_user_1 >= received_doses_user_2).if_else(
        doses_after_vaccination_user_1 - received_doses_user_2,
        doses_after_vaccination_user_1
    )

    # Calculate the new dose allocation after cancellation requests
    doses_after_cancellation_user_1 = doses_after_vaccination_user_2 + canceled_doses_user_1
    doses_after_cancellation_user_2 = doses_after_cancellation_user_1 + canceled_doses_user_2

    # Output the final dose allocation
    final_doses = Output(doses_after_cancellation_user_2, "final_doses", user_1)

    # Output individual vaccinations and cancellations
    vaccinated_doses_user_1 = Output(received_doses_user_1, "vaccinated_doses_user_1", user_1)
    cancelled_doses_user_1 = Output(canceled_doses_user_1, "cancelled_doses_user_1", user_1)
    vaccinated_doses_user_2 = Output(received_doses_user_2, "vaccinated_doses_user_2", user_2)
    cancelled_doses_user_2 = Output(canceled_doses_user_2, "cancelled_doses_user_2", user_2)

    return [
        final_doses,
        vaccinated_doses_user_1,
        cancelled_doses_user_1,
        vaccinated_doses_user_2,
        cancelled_doses_user_2
    ]

print(nada_main())
