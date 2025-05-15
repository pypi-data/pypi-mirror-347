#We twill build the analysis function firs 
class textFormat:
    # Text colors
    GREEN = '\033[92m'
    OKGREEN = '\033[102m'  # Bright green background
    WARNING = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[33m'
    WHITE = '\033[97m'
    BLACK = '\033[30m'

    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_BLACK = '\033[40m'

    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'  # Swap foreground and background colors
    HIDDEN = '\033[8m'  # Invisible text
    STRIKETHROUGH = '\033[9m'

    # Reset/End
    END = '\033[0m'

    # Combine styles
    BOLD_ITALIC = '\033[1m\033[3m'
    BOLD_UNDERLINE = '\033[1m\033[4m'
    ITALIC_UNDERLINE = '\033[3m\033[4m'
    BOLD_ITALIC_UNDERLINE = '\033[1m\033[3m\033[4m'


    @staticmethod
    def rectangle(text, border_char='*', color=None):
        # Ensure 'text' is a string and border_char is also a string
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        
        if not isinstance(border_char, str):
            raise TypeError("border_char must be a string")
        
        # Optional color handling
        color_code = color if color else textFormat.END
        border = border_char * (len(text) + 4)
        return f"{color_code}{border}\n{border_char} {text} {border_char}\n{border}{textFormat.END}"
#---------------------------------------------------------------------------------#
Es = 29000  # ksi
cover = 1.5  # inches
#---------------------------------------------------------------------------------#
import math
import matplotlib
def solve_quadratic(a, b, c):
    # Ensure c is negative
    c = -abs(c)  # Convert c to a negative value
    # Calculate the discriminant
    discriminant = b**2 - 4*a*c
    
    # Check for real roots
    if discriminant < 0:
        return "No real roots"
    
    # Calculate the two roots
    root1 = (-b + math.sqrt(discriminant)) / (2*a)
    root2 = (-b - math.sqrt(discriminant)) / (2*a)
    
    # Return the positive root only
    positive_roots = [r for r in (root1, root2) if r > 0]
    if positive_roots:
        return min(positive_roots)  # Return the smallest positive root
    else:
        return "No positive root"
def calculate_beta(fck):
    """Calculate β₁ based on fc' (in ksi)."""
    if fck <= 4:
        return 0.85
    elif fck <= 5:
        return 0.80
    elif fck <= 6:
        return 0.75
    elif fck <= 7:
        return 0.70
    else:  # fc_prime >= 8000
        return 0.65
#---------------------------------------------------------------------------------#
def calculate_phi(e_t , e_ty):
    """
    Calculate the strength reduction factor (phi) based on the ACI chart.
    e_t: Tensile strain
    e_ty: Yield strain (f_y / E_s)
    """
    if e_t < e_ty:
        print('Compression-controlled region , phi =0.65 ')
        return 0.65             #Compression-controlled region
    elif e_ty <= e_t <= e_ty + 0.003:
        print(' Transition region , phi =calculated ')
        return 0.65 + 0.25 * (e_t - e_ty) / 0.003  # Transition region
    elif e_t > e_ty + 0.003:
        print('Tension-controlled region,, phi =0.9')
        return 0.9  # Tension-controlled region
#---------------------------------------------------------------------------------#
def calculate_As_min(b=None,d=None,fyk=None,fck=None):
    # Calculate the maximum value between (fc^1/3) and 200 psi
    max_value = max(3 * math.sqrt(fck), 200) #psi
    As_min = (b * d /fyk) * max_value
    print(f"Minimum steel area (As_min): {As_min:.2f} square inches")

    return As_min
#---------------------------------------------------------------------------------#
#corbel design based on ACI-318-08
def corbel_design(fck=None, fyk=None, )
    


def analyze_section(b=None, h=None, d=None, As=None, fck=None, fyk=None, 
                    bw=None, hf=None, l=None, s=None, As_prime=0, d_prime=0):
    """
    Section analysis for rectangular, T-sections, and doubly reinforced sections.

    Parameters:
    b : float : Width of rectangular section or flange width for T-section (inches).
    h : float : Total section depth (inches).
    d : float : Effective depth for tension steel (inches).
    As : float : Tension steel area (in²).
    fck : float : Concrete strength (ksi).
    fyk : float : Steel yield strength (ksi).
    bw : float : Width of web for T-section (inches), optional.
    hf : float : Flange thickness for T-section (inches), optional.
    l : float : Span length (feet), optional (for calculating bf if T-section).
    s : float : Spacing or total flange width (inches), optional (for calculating bf if T-section).
    As_prime : float : Compression steel area (in²), optional (default=0).
    d_prime : float : Effective depth for compression steel (inches), optional (default=0).
    Returns:
    dict : Analysis results including phi, Mn, and strain checks.
    """
        # Initialize the variables to avoid UnboundLocalError
    if As_prime != 0 and As_prime is not None:
        print('Section is doubly reinforced section')
    C_c_flange = None
    C_c_web = None
    print(textFormat.UNDERLINE + f'SECTION ANALYSIS :' + textFormat.END)
    
    if bw is not None and hf is not None:  # T-section case
        bf = min(l * 12 / 4, bw + 16 * hf, s) if l and s else None
        print(f'- flang width b = {bf} inch')
        if bf is None:
            raise ValueError("For T-section, provide span length (l) and spacing (s).")
    else:
        bf = b  # Rectangular section case
        print(f'- Section is rectangule section' )

    # Steel forces
    steel_force_tension = As * fyk
    steel_force_compression = As_prime * fyk if As_prime > 0 else 0

    # Determine neutral axis and equivalent stress block depth (a)
    concrete_force = 0.85 * fck * bf #Notice that we used bf 
    a = (steel_force_tension - steel_force_compression) / concrete_force
    beta_1 = calculate_beta(fck)
    c = a / beta_1
    print (f'- Calculated depth of the stress block a ={round(a,2)} in')
    print(f'- Calculated (a,c) value = {a,c} inches')

    # Moment capacity calculation
    if hf is not None and a <= hf:  # Rectangle T-beam Neutral axis within the flange
        # Compression force is entirely in the flange        
        C_c = 0.85 * fck * bf * a  #kips #Compression force in the concrete kips
        M_c = C_c * (d - a / 2)  #in-kip
        print(f'- Section is Rectangular T-Section and Compression force is entirely in the flange')
        print(f'- Calculated Compressive force in concrete C_c ={C_c} , lever arm is d-(a/2) and moment is M_c ={M_c}')
    elif hf is not None and a > hf:  # True T-beam Neutral axis extends into the web
        # Compression force is split between flange and web
        print(f'- Section is (True T-Section) and CCompression force is split between flange and web')
        print(f'- Flange width b = {bf} inch , Force in tension steel = {steel_force_tension} kips')
        Acomp = As *fyk / (0.85 * fck)
        Aflange = hf * bf
        a = hf + (Acomp - Aflange ) / bw
        c = a / beta_1
        C_c_flange = 0.85 * fck * bf * hf #compressionForce by Flange
        C_c_web = 0.85 * fck * bw * (a - hf)
        C_c = C_c_flange + C_c_web    
        M_c = (C_c_flange * (d - hf / 2) +C_c_web * (d - hf - (a - hf) / 2)) #in-kip
        print(f'- Compression force in the flange area = {C_c_flange} kip')
        print(f'- Compression force in the flange area = {C_c_web} kip')   
    else:  # Rectangular section
        C_c = 0.85 * fck * b * a
        M_c = C_c * (d - a / 2) #in-kip
        print(f'- Calculated force in the compression flange C_c = {C_c} kips ')
        print(f'- Compression contribution to the moment M_c = {M_c}in-kip')
    
   #-------------------------------------------------------------------------------#
    # Add steel contributions
    Mn_tensile = steel_force_tension * (d - a / 2) 
    Mn_compression = steel_force_compression * (d - d_prime)  if As_prime > 0 else 0
    Mn = M_c + Mn_compression

    # Check if compression steel yields
    epsilon_prime_c = 0.003 * (c - d_prime) / c  # Strain in compression steel
    epsilon_y = fyk / Es  # Yield strain for steel
    if epsilon_prime_c < epsilon_y:
        print(textFormat.WARNING + f'- Compression steel did not yield. Strain = {round(epsilon_prime_c, 6)} (< {round(epsilon_y, 6)})' + textFormat.END)
        steel_force_compression = epsilon_prime_c * Es * As_prime  # Adjusted compression force
        aa = 0.85*fck*beta_1* b
        bb = As_prime * Es * 0.003  - As * fyk
        cc = As_prime * Es * 0.003 * d_prime
        c = solve_quadratic(aa,bb,cc)
        a = c * beta_1
        C_c = 0.85 * fck * b * a
        M_c = C_c * (d - a / 2) #in-kip
        
        print (f'New Value of C = {c} , New Value of C_c = {C_c}, ')
    else:
        steel_force_compression = fyk * As_prime  # Steel yields, use full yield force

    # Calculate moment contribution of compression steel
    Mn_compression = steel_force_compression * (d - d_prime) if As_prime > 0 else 0

    Mn = M_c + Mn_compression

    
    print(f'- Calculated steel_force_tension = {steel_force_tension} kips')
    print(f'- Calculated steel force compression = {steel_force_compression} kips')
    print(f'- Tensile steel moment contribution = {Mn_tensile} in-kip')
    print(f'- Compression Steel Moment contributio n =  {Mn_compression}kip.ft,{Mn}')
    print(f'- Section forces balanced with {C_c + steel_force_compression - steel_force_tension } unbalanced force ')
    print()
    print(f"{textFormat.BOLD_ITALIC}- Section Nominal Moment capacity =  {Mn} in-kip = {Mn/12} ft-kip {textFormat.END}")
    #-------------------------------------------------------------------------------#

    # Strain calculations
    e_t = 0.003 * (d - c) / c
    e_ty = fyk / Es
    e_limit = e_ty + 0.003
    print()
    print(textFormat.UNDERLINE + 'STRAIN ANALYSIS :' + textFormat.END)
    if e_t > e_limit :
        print(textFormat.GREEN+f'- ACI strain limit was met with strain value of e_t = {round(e_t,6)} above the limiting of {round(e_limit,6)}'+ textFormat.END)
    else:
        print(textFormat.WARNING + f'- ACI strain limit was Not met' + textFormat.END)

    # Check strain in tension steel and whether it yields
    if e_t >= e_ty:
        print(textFormat.GREEN + f'- Tension steel yielded with strain {round(e_t, 6)} (>= {round(epsilon_y, 6)})' + textFormat.END)
    else:
        print(textFormat.WARNING + f'- Tension steel did not yield, strain = {round(e_t, 6)} (< {round(epsilon_y, 6)})' + textFormat.END)

    phi = calculate_phi(e_t, e_ty)
    phi_Mn = phi * Mn /12 #ft-kip
    print(f'- calculated phi = {phi}')
    print(textFormat.BOLD_ITALIC + f'- Calculated section Capacity phi_Mn = {round(phi_Mn,2)} ft-kip'+textFormat.END)
    #-------------------------------------------------------------------------------#
    
    # Check minimum steel for rectangular or T-section
    if hf is not None and bw is not None:
        effective_b = bw
    else:
        effective_b = b

    As_min = calculate_As_min(effective_b, h - cover, fyk * 1000, fck * 1000)
    steel_sufficient = As >= As_min
#rho value is missing here do we need it ?we simply solve for it!
#maybe we can make a section for ACI requirement   
    # Results
    results = {
        "section_type": "T-section" if bw is not None and hf is not None else "Rectangular",
        "bf": bf,
        "phi": phi,
        "Mn": Mn,
        "c": c,
        "e_t": e_t,
        "steel_sufficient": steel_sufficient,
        "As_min": As_min
    }
    return results
#the final oourput for this function should be phiMn and design efficiency 
    #-------------------------------------------------------------------------------#
    # def analyse_col_sec(width=None, length=None,fyk=None , fck=None )
    #     phi



if __name__ == "__main__":
    result = analyze_section( b=12, h=24, d=20, As=4, fck=4000, fyk=50000,
    bw=10, hf=6, l=15, s=6, As_prime=2, d_prime=2)
    print(result)